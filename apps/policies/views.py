from rest_framework import generics, permissions
from core.responses import ApiResponse, get_lang
from core.permissions import IsExpert, IsAdminRole
from .models import RolePolicy, AppPolicy, FeedbackReport
from .serializers import RolePolicySerializer, AppPolicySerializer, FeedbackSerializer
from .services import PolicyService

class MyPolicyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lang = get_lang(request)
        user = request.user

        # Admin يأخذ سياسة الـ Expert
        role = user.role
        if role == 'admin':
            role = 'expert'

        policy = PolicyService.get_policy(role)

        if not policy:
            return ApiResponse.not_found(lang=lang)

        serializer = RolePolicySerializer(policy)
        remaining  = PolicyService.get_remaining_scans(user=user)

        return ApiResponse.success(data={
            "role":                  user.role,
            "role_level":            user.role_level,
            "remaining_scans_today": remaining,
            "policy":                serializer.data,
        }, lang=lang)
    
class AllPoliciesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset           = RolePolicy.objects.all()
    serializer_class   = RolePolicySerializer

    def list(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(data=serializer.data, lang=lang)


class AppPolicyView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset           = AppPolicy.objects.filter(is_active=True)
    serializer_class   = AppPolicySerializer

    def list(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(
            data=serializer.data,
            message_key='app_policy_fetched',
            lang=lang
        )


class FeedbackCreateView(generics.CreateAPIView):
    """الخبير يبلغ عن نتيجة خاطئة"""
    serializer_class   = FeedbackSerializer
    permission_classes = [IsExpert]

    def perform_create(self, serializer):
        serializer.save(expert=self.request.user)

    def create(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return ApiResponse.created(
            data=serializer.data,
            message="تم إرسال التقرير بنجاح — شكراً على مساهمتك",
            lang=lang
        )


class FeedbackListView(generics.ListAPIView):
    """Admin يرى كل التقارير"""
    serializer_class   = FeedbackSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        return FeedbackReport.objects.select_related('expert', 'scan').all()

    def list(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(data=serializer.data, lang=lang)


class MyFeedbackView(generics.ListAPIView):
    """الخبير يرى تقاريره"""
    serializer_class   = FeedbackSerializer
    permission_classes = [IsExpert]

    def get_queryset(self):
        return FeedbackReport.objects.filter(expert=self.request.user)

    def list(self, request, *args, **kwargs):
        lang       = get_lang(request)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return ApiResponse.success(data=serializer.data, lang=lang)