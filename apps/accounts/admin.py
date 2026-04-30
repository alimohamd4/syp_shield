from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display    = ['email', 'full_name', 'tier', 'tier_level', 'is_active', 'date_joined']
    list_filter     = ['tier', 'is_active', 'is_staff']
    search_fields   = ['email', 'full_name']
    ordering        = ['-date_joined']

    fieldsets = (
        ('معلومات الدخول', {'fields': ('email', 'password')}),
        ('المعلومات الشخصية', {'fields': ('full_name', 'avatar')}),
        ('الصلاحيات', {'fields': ('tier', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'tier', 'password1', 'password2'),
        }),
    )