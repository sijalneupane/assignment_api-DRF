from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

class TeacherPermission(permissions.BasePermission):
    """Permission class for teachers and admins"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated("Authentication required")
        if not (hasattr(request.user, 'role') and request.user.role in ['teacher', 'admin']):
            raise PermissionDenied("Teacher or admin role required")
        return True

class AdminOnlyPermission(permissions.BasePermission):
    """Permission class for admin-only operations"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated("Authentication required")
        if not (hasattr(request.user, 'role') and request.user.role == 'admin'):
            raise PermissionDenied("Admin role required")
        return True

class AdminOrTeacherPermission(permissions.BasePermission):
    """Permission class for teachers and admins"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated("Authentication required")
        if not (hasattr(request.user, 'role') and request.user.role in ['teacher', 'admin']):
            raise PermissionDenied("Teacher or admin role required")
        return True