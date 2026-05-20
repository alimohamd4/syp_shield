from rest_framework.permissions import BasePermission


class IsGuest(BasePermission):
    message = "هذه الميزة للزوار فقط"

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAuthenticatedUser(BasePermission):
    message = "يجب تسجيل الدخول أولاً"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role_level >= 1


class IsExpert(BasePermission):
    message = "هذه الميزة للخبراء فقط"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role_level >= 2


class IsAdminRole(BasePermission):
    message = "هذه الميزة للمديرين فقط"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'