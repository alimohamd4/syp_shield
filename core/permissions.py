from rest_framework.permissions import BasePermission


class IsObsidianTier(BasePermission):
    message = "هذه الميزة متاحة لمستخدمي Obsidian فقط"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tier == 'obsidian'


class IsGoldOrAbove(BasePermission):
    message = "هذه الميزة متاحة لمستخدمي Gold و Obsidian فقط"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tier_level >= 2


class IsStandardOrAbove(BasePermission):
    message = "يجب تسجيل الدخول أولاً"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tier_level >= 1