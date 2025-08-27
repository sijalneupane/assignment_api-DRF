from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from .models import Notices
from .serializers import NoticeWriteSerializer, NoticeReadSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
    
@extend_schema(
    summary="Create new notice",
    description="Create a new notice. Only admin and teachers can create notices.",
    request=NoticeWriteSerializer,
    examples=[
        OpenApiExample(
            'Notice Creation Example',
            summary='Create notice request',
            description='Example request body for creating a new notice',
            value={
                "title": "Important Notice",
                "description": "This is an important notice for all students.",
                "subject": "General",
                "faculty": "All",
                "semester": "All"
            },
            request_only=True,
        )
    ],
    tags=['Notices']
)
class NoticeCreateView(CreateAPIView):
    """Create a new notice - only for admin/teacher"""
    permission_classes = [IsAuthenticated]
    serializer_class = NoticeWriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.role not in ['admin', 'teacher']:
                raise PermissionDenied("Only admin and teachers can create notices.")
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                notice = serializer.save(issued_by=user)
                response_serializer = NoticeReadSerializer(notice)
                return Response({
                    'data': response_serializer.data,
                    'message': 'Notice created successfully'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': 'Validation error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'Failed to create notice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@extend_schema(
    summary="Get all notices",
    description="Retrieve all notices with issuer details. Accessible to all authenticated users.",
    tags=['Notices']
)
class NoticeListView(ListAPIView):
    """List all notices with user details"""
    permission_classes = [IsAuthenticated]
    serializer_class = NoticeReadSerializer
    
    def get_queryset(self):
        return Notices.objects.select_related('issued_by').all().order_by('-updated_at')
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Notices retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve notices'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@extend_schema(
    summary="Get notice by ID",
    description="Retrieve a specific notice by its ID",
    tags=['Notices']
)
class NoticeDetailView(RetrieveAPIView):
    """Retrieve a specific notice by ID"""
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()
    serializer_class = NoticeReadSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': 'Notice retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Notices.DoesNotExist:
            raise NotFound("Notice not found")
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve notice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@extend_schema(
    summary="Update notice",
    description="Update an existing notice. Only the creator or admin can update notices.",
    request=NoticeWriteSerializer,
    examples=[
        OpenApiExample(
            'Notice Update Example',
            summary='Update notice request',
            description='Example request body for updating a notice',
            value={
                "title": "Updated Important Notice",
                "description": "This is an updated important notice for all students.",
                "subject": "General",
                "faculty": "All",
                "semester": "All"
            },
            request_only=True,
        )
    ],
    tags=['Notices']
)
class NoticeUpdateView(UpdateAPIView):
    """Update a notice - only by creator or admin"""
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()
    serializer_class = NoticeWriteSerializer
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            
            if user != instance.issued_by and user.role != 'admin':
                raise PermissionDenied("You can only update your own notices.")
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                notice = serializer.save()
                response_serializer = NoticeReadSerializer(notice)
                return Response({
                    'data': response_serializer.data,
                    'message': 'Notice updated successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'message': 'Validation error',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Notices.DoesNotExist:
            raise NotFound("Notice not found")
        except Exception as e:
            return Response({
                'message': 'Failed to update notice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@extend_schema(
    summary="Delete notice",
    description="Delete an existing notice by its ID. Only the creator or admin can delete notices.",
    tags=['Notices']
)
class NoticeDeleteView(DestroyAPIView):
    """Delete a notice - only by creator or admin"""
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()  

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            
            if user != instance.issued_by and user.role != 'admin':
                raise PermissionDenied("You can only delete your own notices.")
            
            instance.delete()
            return Response({
                'message': 'Notice deleted successfully'
            }, status=status.HTTP_200_OK)
        except Notices.DoesNotExist:
            raise NotFound("Notice not found")
        except Exception as e:
            return Response({
                'message': 'Failed to delete notice'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)