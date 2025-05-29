from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,CreateAPIView,ListAPIView
from rest_framework.exceptions import PermissionDenied
from .models import Notices
from .serializers import NoticeWriteSerializer, NoticeReadSerializer

class NoticeListCreateView(ListCreateAPIView):
    """
    GET: List all notices (for all authenticated users)
    POST: Create notice (only for admin/teacher)
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notices.objects.select_related('issued_by').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NoticeReadSerializer
        return NoticeWriteSerializer
    
    def perform_create(self, serializer):
        # Check if user has permission to create notices
        user = self.request.user
        if user.role not in ['admin', 'teacher']:
            raise PermissionDenied("Only admin and teachers can create notices.")
        
        # Set issued_by to current user from JWT token
        serializer.save(issued_by=user)

class NoticeDetailView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single notice
    PUT/PATCH: Update notice (only by creator or admin)
    DELETE: Delete notice (only by creator or admin)
    """
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NoticeReadSerializer
        return NoticeWriteSerializer
    
    def perform_update(self, serializer):
        # Check if user can update this notice
        user = self.request.user
        notice = self.get_object()
        
        if user != notice.issued_by and user.role != 'admin':
            raise PermissionDenied("You can only update your own notices.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        # Check if user can delete this notice
        user = self.request.user
        
        if user != instance.issued_by and user.role != 'admin':
            raise PermissionDenied("You can only delete your own notices.")
        
        instance.delete()

# Alternative: If you want separate views for different operations
class NoticeCreateView(CreateAPIView):
    """Create notice - extracts user from JWT token"""
    permission_classes = [IsAuthenticated]
    serializer_class = NoticeWriteSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role not in ['admin', 'teacher']:
            raise PermissionDenied("Only admin and teachers can create notices.")
        
        serializer.save(issued_by=user)

class NoticeListView(ListAPIView):
    """List all notices with user details"""
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()
    serializer_class = NoticeReadSerializer