from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # تم إزالة الحقول غير المعرفة لتجنب تعطل السيرفر
    list_display    = ['email', 'full_name', 'is_active', 'date_joined']
    list_filter     = ['is_active', 'is_staff']
    search_fields   = ['email', 'full_name']
    ordering        = ['-date_joined']

    # تم إزالة الحقول التي تسبب المشكلة من صناديق العرض بداخل الأدمن
    fieldsets = (
        ('معلومات الدخول', {'fields': ('email', 'password')}),
        ('المعلومات الشخصية', {'fields': ('full_name', 'avatar')}),
        ('الصلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )