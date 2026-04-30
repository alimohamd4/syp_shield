from django.contrib import admin
from .models import TierPolicy, ScanLimit, AppPolicy


@admin.register(TierPolicy)
class TierPolicyAdmin(admin.ModelAdmin):
    list_display = ['tier', 'daily_scan_limit', 'history_days',
                    'can_view_heatmap', 'can_export_report', 'can_view_mse']
    ordering     = ['tier']


@admin.register(ScanLimit)
class ScanLimitAdmin(admin.ModelAdmin):
    list_display  = ['user', 'date', 'scan_count']
    list_filter   = ['date']
    search_fields = ['user__email']


@admin.register(AppPolicy)
class AppPolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'is_active', 'updated_at']
    ordering     = ['order']