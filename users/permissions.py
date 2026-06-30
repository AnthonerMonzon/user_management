from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Only allows SuperAdmin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superadmin()


class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Allows SuperAdmin to perform any action, others can only read.
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_superadmin()
