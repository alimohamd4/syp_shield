from rest_framework import serializers
from .models import RolePolicy, AppPolicy, FeedbackReport


class RolePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model  = RolePolicy
        fields = [
            'role', 'daily_scan_limit', 'history_days',
            'can_view_heatmap', 'can_view_mse',
            'can_export_report', 'can_give_feedback',
            'description',
        ]


class AppPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model  = AppPolicy
        fields = ['section', 'title', 'content', 'icon', 'order']


class FeedbackSerializer(serializers.ModelSerializer):
    expert_name = serializers.CharField(source='expert.full_name', read_only=True)
    scan_result = serializers.CharField(source='scan.result',      read_only=True)

    class Meta:
        model  = FeedbackReport
        fields = ['id', 'scan', 'note', 'status', 'expert_name', 'scan_result', 'created_at']
        read_only_fields = ['status', 'expert_name', 'scan_result', 'created_at']