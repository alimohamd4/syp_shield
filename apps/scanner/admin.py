from django.contrib import admin
from .models import ScanSession


@admin.register(ScanSession)
class ScanSessionAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'result', 'mse_score', 'status', 'created_at']
    list_filter   = ['result', 'status']
    search_fields = ['user__email', 'user__full_name']
    ordering      = ['-created_at']
    readonly_fields = ['mse_score', 'confidence', 'created_at', 'updated_at']