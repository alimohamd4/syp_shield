from rest_framework import generics, permissions
from core.responses import ApiResponse, get_lang
from .models import TierPolicy, AppPolicy
from .serializers import TierPolicySerializer, AppPolicySerializer
from .services import PolicyService


class MyPolicyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lang = get_lang(request)
        policy = PolicyService.get_policy(request.user.tier)

        if not policy:
            return ApiResponse.not_found(
                message_key='policy_not_found',
                lang=lang
            )

        serializer = TierPolicySerializer(policy)
        remaining  = PolicyService.get_remaining_scans(request.user)

        return ApiResponse.success(
            data={
                "tier":                  request.user.tier,
                "tier_level":            request.user.tier_level,
                "remaining_scans_today": remaining,
                "policy":                serializer.data,
            },
            message_key='policy_fetched',
            lang=lang
        )


class AllPoliciesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset           = TierPolicy.objects.all()
    serializer_class   = TierPolicySerializer

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        queryset   = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(
            data=serializer.data,
            message_key='success',
            lang=lang
        )


class AppPolicyView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset           = AppPolicy.objects.filter(is_active=True)
    serializer_class   = AppPolicySerializer

    def list(self, request, *args, **kwargs):
        lang = get_lang(request)
        queryset   = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return ApiResponse.success(
            data=serializer.data,
            message_key='app_policy_fetched',
            lang=lang
        )