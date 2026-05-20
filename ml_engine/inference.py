import torch
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
import torchvision.transforms as T
import os

from .model.deepcae import DeepCAE
from .gradcam import GradCAM_AE

class SyrianCurrencyValidator:
    def __init__(self, model_weights_path, references_dir):
        """
        Initialize the validator, load the model, Grad-CAM, and SIFT references.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = DeepCAE().to(self.device)
        
        if not os.path.exists(model_weights_path):
            raise FileNotFoundError(f"Model weights not found at {model_weights_path}")
            
        self.model.load_state_dict(torch.load(model_weights_path, map_location=self.device))
        self.model.eval()
        
        self.grad_cam = GradCAM_AE(self.model, self.model.encoder[12])
        
        self.THRESHOLD = 0.05802 
        self.TARGET_SIZE = (256, 256)
        self.transform = T.Compose([
            T.Resize(self.TARGET_SIZE),
            T.ToTensor()
        ])

        # ---------------------------------------------------------
        # تهيئة SIFT وحفظ بصمات الصور المرجعية في الذاكرة لتسريع السيرفر
        # ---------------------------------------------------------
        self.sift = cv2.SIFT_create()
        self.flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))
        self.reference_data = self._preload_references(references_dir)

    def _preload_references(self, ref_dir):
        """Pre-computes SIFT keypoints and descriptors for all reference images."""
        ref_data = []
        if not os.path.exists(ref_dir):
            print(f"Warning: Reference directory {ref_dir} not found. Cropping will fail.")
            return ref_data

        for file in os.listdir(ref_dir):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(ref_dir, file)
                img = cv2.imread(img_path)
                if img is not None:
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    kp, des = self.sift.detectAndCompute(gray, None)
                    if des is not None:
                        ref_data.append({'img': img, 'kp': kp, 'des': des, 'name': file})
        return ref_data

    def _crop_and_align(self, raw_img_cv2):
        """Uses SIFT to find the banknote in the raw image and crop it."""
        if raw_img_cv2 is None or not self.reference_data:
            return None

        gray_test = cv2.cvtColor(raw_img_cv2, cv2.COLOR_BGR2GRAY)
        kp_test, des_test = self.sift.detectAndCompute(gray_test, None)
        
        if des_test is None:
            return None

        best_aligned = None
        max_matches = 0

        for ref in self.reference_data:
            matches = self.flann.knnMatch(ref['des'], des_test, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

            if len(good_matches) > 15 and len(good_matches) > max_matches:
                src_pts = np.float32([ref['kp'][m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp_test[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                
                M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
                if M is not None:
                    h, w = ref['img'].shape[:2]
                    aligned = cv2.warpPerspective(raw_img_cv2, M, (w, h))
                    best_aligned = cv2.resize(aligned, self.TARGET_SIZE, interpolation=cv2.INTER_AREA)
                    max_matches = len(good_matches)

        return best_aligned # ترجع الصورة المقصوصة أو None إذا لم تكتشف عملة

    def _tensor_to_base64_heatmap(self, original_tensor, cam_mask):
        """Helper method to generate a base64 string of the superimposed heatmap."""
        heatmap = np.uint8(255 * cam_mask)
        colored_heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        img_display = original_tensor.squeeze().cpu().detach().numpy().transpose(1, 2, 0)
        img_display = np.uint8(255 * img_display)
        img_bgr = cv2.cvtColor(img_display, cv2.COLOR_RGB2BGR)
        
        superimposed = cv2.addWeighted(img_bgr, 0.6, colored_heatmap, 0.4, 0)
        superimposed_rgb = cv2.cvtColor(superimposed, cv2.COLOR_BGR2RGB)
        
        result_img = Image.fromarray(superimposed_rgb)
        buffered = BytesIO()
        result_img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def validate_image(self, pil_image):
        """
        Main method to be called by Django Views.
        Accepts a RAW PIL Image, crops it, and returns validation results.
        """
        # 1. تحويل الصورة من PIL إلى CV2 للقص
        cv2_img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # 2. قص الصورة باستخدام SIFT
        cropped_cv2_img = self._crop_and_align(cv2_img)
        
        if cropped_cv2_img is None:
            # إذا لم يتعرف الـ SIFT على عملة، نرجع خطأ للواجهة
            return {
                "status": "error",
                "message": "لم يتم التعرف على عملة سورية في الصورة، يرجى التأكد من وضوح الصورة وتوجيه الكاميرا بشكل صحيح."
            }

        # 3. تجهيز الصورة المقصوصة للنموذج
        cropped_pil = Image.fromarray(cv2.cvtColor(cropped_cv2_img, cv2.COLOR_BGR2RGB))
        img_tensor = self.transform(cropped_pil).unsqueeze(0).to(self.device)
        
        # 4. تشغيل الغراد كام والتحليل
        cam_mask = self.grad_cam.generate_cam(img_tensor)
        
        with torch.no_grad():
            output = self.model(img_tensor)
            rmse_error = torch.sqrt(((output - img_tensor)**2).mean(dim=[1, 2, 3]) + 1e-6).item()
            
        is_real = bool(rmse_error <= self.THRESHOLD)
        confidence = max(0, min(100, 100 - ((rmse_error / self.THRESHOLD) * 50))) if is_real else max(0, min(100, (rmse_error / self.THRESHOLD) * 50))

        heatmap_base64 = self._tensor_to_base64_heatmap(img_tensor, cam_mask)
        
        return {
            "status": "success",
            "data": {
                "is_genuine": is_real,
                "anomaly_score": round(rmse_error, 5),
                "threshold_applied": self.THRESHOLD,
                "confidence_percentage": round(confidence, 2),
                "heatmap_image_base64": heatmap_base64
            }
        }