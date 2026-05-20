from django.contrib import admin
from .models import RolePolicy, ScanLimit, AppPolicy, FeedbackReport


@admin.register(RolePolicy)
class RolePolicyAdmin(admin.ModelAdmin):
    list_display = ['role', 'daily_scan_limit', 'history_days',
                    'can_view_heatmap', 'can_view_mse',
                    'can_give_feedback']
    ordering     = ['role']


@admin.register(ScanLimit)
class ScanLimitAdmin(admin.ModelAdmin):
    list_display  = ['user', 'device_id', 'date', 'scan_count']
    list_filter   = ['date']
    search_fields = ['user__email', 'device_id']


@admin.register(AppPolicy)
class AppPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'is_active']
    ordering     = ['order']


@admin.register(FeedbackReport)
class FeedbackReportAdmin(admin.ModelAdmin):
    list_display  = ['expert', 'scan', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['expert__email']
    actions       = ['mark_reviewed', 'mark_rejected']

    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
    mark_reviewed.short_description = "تعيين كـ Reviewed"

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = "تعيين كـ Rejected"