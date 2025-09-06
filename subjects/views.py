from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from django.db import transaction
from .models import Subject
from .serializers import SubjectSerializer, SubjectCreateUpdateSerializer
from utils.custompermissions import AdminOnlyPermission
from drf_spectacular.utils import extend_schema, OpenApiExample

@extend_schema(
    summary="Get all subjects",
    description="Retrieve all subjects. Accessible to all authenticated users.",
    tags=['Subjects']
)
class SubjectListView(generics.ListAPIView):
    """
    List all subjects - accessible to all authenticated users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Subjects retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve subjects'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
@extend_schema(
    summary="Get subject by ID",
    description="Retrieve a specific subject by its ID",
    tags=['Subjects']
)
class SubjectDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific subject - accessible to all authenticated users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                'data': serializer.data,
                'message': 'Subject retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            raise NotFound("Subject not found")
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve subject'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
@extend_schema(
    summary="Create new subject",
    description="Create a new subject. Only admin users can create subjects.",
    request=SubjectCreateUpdateSerializer,
    examples=[
        OpenApiExample(
            'Subject Creation Example',
            summary='Create subject request',
            description='Example request body for creating a new subject',
            value={
                "name": "Computer Networks",
                "code": "CN101",
                "credit_hours": 3,
                "description": "Introduction to Computer Networks"
            },
            request_only=True,
        )
    ],
    tags=['Subjects']
)
class SubjectCreateView(generics.CreateAPIView):
    """
    Create a new subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOnlyPermission]


    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    subject = serializer.save(created_by=request.user)
                    response_serializer = SubjectSerializer(subject)
                    return Response({
                        'data': response_serializer.data,
                        'message': 'Subject created successfully'
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'message': 'Validation error',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'message': 'Failed to create subject'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Update subject",
    description="Update an existing subject. Only admin users can update subjects.",
    request=SubjectCreateUpdateSerializer,
    examples=[
        OpenApiExample(
            'Subject Update Example',
            summary='Update subject request',
            description='Example request body for updating a subject',
            value={
                "name": "Advanced Computer Networks",
                "code": "ACN101",
                "credit_hours": 4,
                "description": "Advanced study of computer networks"
            },
            request_only=True,
        )
    ],
    tags=['Subjects']
)
class SubjectUpdateView(generics.UpdateAPIView):
    """
    Update a subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOnlyPermission]

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    subject = serializer.save()
                    response_serializer = SubjectSerializer(subject)
                    return Response({
                        'message': 'Subject updated successfully',
                        'data': response_serializer.data,
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Validation error',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            raise NotFound("Subject not found")
        except Exception as e:
            return Response({
                'message': 'Failed to update subject'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Delete subject",
    description="Delete an existing subject by its ID. Only admin users can delete subjects.",
    tags=['Subjects']
)

class SubjectDeleteView(generics.DestroyAPIView):
    """
    Delete a subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    permission_classes = [AdminOnlyPermission,IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
                return Response({
                    'message': 'Subject deleted successfully'
                }, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            raise NotFound("Subject not found")
        except Exception as e:
            print(e)
            return Response({
                'message': 'Failed to delete subject',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
