from rest_framework import generics, permissions
from core.responses import ApiResponse, get_lang
from core.permissions import IsAdminRole
from .models import ScanSession
from .serializers import ScanCreateSerializer, ScanResultSerializer
from .statistics import SystemStatistics
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ScanCreateView(generics.CreateAPIView):
    serializer_class   = ScanCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        scan = serializer.save(user=self.request.user, status='processing')
        self._run_inference(scan)

    def _run_inference(self, scan):
        try:
            from ml_engine import get_validator

            # تحميل الصورة
            pil_image = Image.open(scan.image.path).convert('RGB')

            # تشغيل النموذج
            validator = get_validator()
            result    = validator.validate_image(pil_image)

            if result['status'] == 'error':
                scan.status = 'failed'
                scan.notes  = result['message']
                scan.save()
                return

            data = result['data']

            # حفظ النتائج
            scan.status     = 'completed'
            scan.result     = 'genuine' if data['is_genuine'] else 'counterfeit'
            scan.mse_score  = data['anomaly_score']
            scan.threshold  = data['threshold_applied']
            scan.confidence = data['confidence_percentage']

            # حفظ الـ Heatmap
            if data.get('heatmap_image_base64'):
                import base64, os
                from django.conf import settings

                heatmap_dir  = os.path.join(settings.MEDIA_ROOT, 'heatmaps')
                os.makedirs(heatmap_dir, exist_ok=True)

                heatmap_path = os.path.join(heatmap_dir, f'{scan.id}_heatmap.jpg')
                with open(heatmap_path, 'wb') as f:
                    f.write(base64.b64decode(data['heatmap_image_base64']))

                scan.heatmap = f'heatmaps/{scan.id}_heatmap.jpg'

            scan.save()

        except Exception as e:
            logger.error(f"ML Inference Error: {e}")
            scan.status = 'failed'
            scan.notes  = str(e)
            scan.save()

    def create(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        scan = ScanSession.objects.filter(user=request.user).latest('created_at')

        if scan.status == 'failed':
            return ApiResponse.error(
                message=scan.notes or "فشل تحليل الصورة",
                lang=lang
            )

        result_serializer = ScanResultSerializer(scan)
        return ApiResponse.created(
            data=result_serializer.data,
            message_key='scan_success',
            lang=lang
        )


class ScanHistoryView(generics.ListAPIView):
    serializer_class   = ScanResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScanSession.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(
            data=serializer.data,
            message_key='scan_history',
            lang=lang
        )


class ScanDetailView(generics.RetrieveAPIView):
    serializer_class   = ScanResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScanSession.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        lang       = get_lang(request)
        instance   = self.get_object()
        serializer = self.get_serializer(instance)
        return ApiResponse.success(data=serializer.data, lang=lang)


class AdminStatisticsView(generics.GenericAPIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        lang = get_lang(request)
        data = {
            "daily":    SystemStatistics.get_daily_stats(),
            "users":    SystemStatistics.get_users_stats(),
            "feedback": SystemStatistics.get_feedback_stats(),
            "overall":  SystemStatistics.get_overall_stats(),
        }
        return ApiResponse.success(
            data=data,
            message="تم جلب الإحصائيات بنجاح",
            lang=lang
        )