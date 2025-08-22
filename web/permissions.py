from rest_framework import permissions

class IsJWTCAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        