from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound,ParseError
from .models import Notices
from .serializers import NoticeReadSerializer,NoticeCreateSerializer,NoticeUpdateSerializer
from drf_spectacular.utils import extend_schema
from utils.custompermissions import AdminOrTeacherPermission
from fileandimage.models import FileAndImage
from fileandimage.views import FileAndImageDeleteView
from rest_framework import serializers
@extend_schema(
    summary="Create new notice",
    description="Create a new notice. Only admin and teachers can create notices.",
    request=NoticeCreateSerializer,
    tags=['Notices']
)
class NoticeCreateView(CreateAPIView):
    """Create a new notice - only for admin/teacher"""
    permission_classes = [IsAuthenticated, AdminOrTeacherPermission ]
    serializer_class = NoticeCreateSerializer
    # parser_classes=[MultiPartParser,FormParser]
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.role not in ['admin', 'teacher']:
                raise PermissionDenied("Only admin and teachers can create notices.")
            
            serializer = self.get_serializer(data=request.data)
            
            if serializer.is_valid():
                notice = serializer.save(issued_by=user)
                print("Notice created:", notice)
                response_serializer = NoticeReadSerializer(notice)
                return Response({
                    'data': response_serializer.data,
                    'message': 'Notice created successfully'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except (NotFound) as e:
            raise NotFound({"message": str(e)})
        except (ValidationError, ParseError, serializers.ValidationError) as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
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
                'message': str(e)
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
            raise NotFound({"message": "Notice not found"})
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@extend_schema(
    summary="Update notice",
    description="Update an existing notice. Only the creator or admin can update notices.",
    request=NoticeUpdateSerializer,
    tags=['Notices']
)
class NoticeUpdateView(UpdateAPIView):
    """Update a notice - only by creator or admin"""
    permission_classes = [IsAuthenticated]
    queryset = Notices.objects.select_related('issued_by').all()
    serializer_class = NoticeUpdateSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            
            if user != instance.issued_by and user.role != 'admin':
                raise PermissionDenied({"message": "You can only update your own notices."})
            
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
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        except Notices.DoesNotExist:
            raise NotFound({"message": "Notice not found"})
        except (NotFound) as e:
            raise NotFound({"message": str(e)})
        except (ValidationError, ParseError, serializers.ValidationError) as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': str(e)
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
    serializer_class=NoticeReadSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user

            if user != instance.issued_by and user.role != 'admin':
                raise PermissionDenied({"message": "You can only delete your own notices."})
            
            # Delete the associated file/image if it exists
            if instance.notice_image:
                # You might want to call the appropriate delete method for FileAndImage
                # FileAndImageDeleteView.delete(self, request, pk=instance.notice_image.file_id)
                pass
                
            instance.delete()
            return Response({
                'message': 'Notice deleted successfully'
            }, status=status.HTTP_200_OK)
        except Notices.DoesNotExist:
            raise NotFound({"message": "Notice not found"})
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)