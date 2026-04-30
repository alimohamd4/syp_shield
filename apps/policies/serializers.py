from rest_framework import serializers
from .models import TierPolicy, AppPolicy


class TierPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model  = TierPolicy
        fields = [
            'tier',
            'daily_scan_limit',
            'history_days',
            'can_view_heatmap',
            'can_export_report',
            'can_view_mse',
            'description',
        ]


class AppPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model  = AppPolicy
        fields = ['section', 'title', 'content', 'icon', 'order']