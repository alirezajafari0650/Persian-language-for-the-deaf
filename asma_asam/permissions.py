from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_superuser
        )


class IsSpecialUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_special or
            request.user.is_superuser
        )


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and
            request.user.is_authenticated
        )
