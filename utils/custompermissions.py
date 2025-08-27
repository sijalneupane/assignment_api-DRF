from rest_framework import permissions
from .customresponse import ForbiddenException, UnauthorizedException

class TeacherPermission(permissions.BasePermission):
    """Permission class for teachers and admins"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return UnauthorizedException("Authentication required")
        if not (hasattr(request.user, 'role') and request.user.role in ['teacher', 'admin']):
            return ForbiddenException("Teacher or admin role required")
        return True

class AdminOnlyPermission(permissions.BasePermission):
    """Permission class for admin-only operations"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return UnauthorizedException("Authentication required")
        if not (hasattr(request.user, 'role') and request.user.role == 'admin'):
            return ForbiddenException("Admin role required")
        return True