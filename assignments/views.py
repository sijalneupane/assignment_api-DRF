
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.db import transaction
from .models import Assignment, Subject, CustomDevice
from core.models import CustomUser
from .serializers import AssignmentCreateSerializer, AssignmentSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from utils.custompermissions import TeacherPermission

@extend_schema(
    summary="Create new assignment",
    description="Add a new assignment. Only teachers and admins can create assignments.",
    request=AssignmentCreateSerializer,
    examples=[
        OpenApiExample(
            'Assignment Creation Example',
            summary='Create assignment request',
            description='Example request body for creating a new assignment',
            value={
                "title": "Computer Network Assignment",
                "description": "Complete exercises 1-10 from chapter 3. Show all your work.",
                "subject_name": "C programming",
                "semester": "First Semester",
                "faculty": "BCA"
            },
            request_only=True,
        )
    ],
    tags=['Assignments']
)
class AssignmentCreateView(generics.CreateAPIView):
    """API View to create new assignments"""
    permission_classes = [permissions.IsAuthenticated, TeacherPermission]
    serializer_class = AssignmentCreateSerializer
    queryset = Assignment.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                data = request.data.copy()
                # Don't set teacher in data, we'll set it when saving
                
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    assignment = serializer.save(teacher=request.user)
                    response_serializer = AssignmentCreateSerializer(assignment)
                    return Response({
                        'data': response_serializer.data,
                        'message': 'Assignment created successfully'
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'message': 'Validation error',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            raise NotFound("Subject not found")
        except Exception as e:
            print(e)
            return Response({
                'message': 'Failed to create assignment',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Get all assignments",
    description="Retrieve all assignments with subject and teacher details",
    tags=['Assignments']
)
class AssignmentListView(generics.ListAPIView):
    """API View to retrieve all assignments"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all().order_by("created_at").reverse()

    def list(self, request, *args, **kwargs):
        try:
            assignments = self.get_queryset()
            data = []
            for assignment in assignments:
                serializer = self.get_serializer(assignment)
                assignment_data = dict(serializer.data)
                # assignment_data['subjectName'] = assignment.subject.name
                # assignment_data['teacher'] = assignment.teacher.name
                # assignment_data['teacherId'] = assignment.teacher.id
                data.append(assignment_data)
            return Response({
                'data': data,
                'message': 'Assignments retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve assignments'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Get assignment by ID",
    description="Retrieve a specific assignment by its ID",
    tags=['Assignments']
)
class AssignmentDetailView(generics.RetrieveAPIView):
    """API View to retrieve assignment by ID"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            assignment = self.get_object()
            serializer = self.get_serializer(assignment)
            assignment_data = dict(serializer.data)
            # assignment_data['subjectName'] = assignment.subject.name
            # assignment_data['teacher'] = assignment.teacher.name
            # assignment_data['teacherId'] = assignment.teacher.id
            return Response({
                'data': assignment_data,
                'message': 'Assignment retrieved successfully'
            }, status=status.HTTP_200_OK)
        except Assignment.DoesNotExist:
            raise NotFound("Assignment not found")
        except Exception as e:
            return Response({
                'message': 'Failed to retrieve assignment'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Update assignment",
    description="Update an existing assignment. Only teachers and admins can update assignments.",
    request=AssignmentCreateSerializer,
    examples=[
        OpenApiExample(
            'Assignment Update Example',
            summary='Update assignment request',
            description='Example request body for updating an assignment',
            value={
                "title": "Updated Computer Network Assignment",
                "description": "Complete exercises 1-15 from chapter 3. Show all your work.",
                "subjectName": "Computer Network",
                "semester": "First Semester",
                "faculty": "BCA"
            },
            request_only=True,
        )
    ],
    tags=['Assignments']
)

class AssignmentUpdateView(generics.UpdateAPIView):
    """API View to update assignments"""
    permission_classes = [permissions.IsAuthenticated, TeacherPermission]
    serializer_class = AssignmentCreateSerializer
    queryset = Assignment.objects.all()
    
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                assignment = self.get_object()
                data = request.data.copy()
                
                try:
                    subject = Subject.objects.get(name=data['subjectName'])
                    data['subject'] = subject.id
                    data['teacher'] = request.user.id
                except Subject.DoesNotExist:
                    raise NotFound("Subject not found")
                except KeyError:
                    return Response({
                        'message': 'subjectName is required'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                serializer = self.get_serializer(assignment, data=data, partial=True)
                if serializer.is_valid():
                    updated_assignment = serializer.save()
                    response_serializer = AssignmentSerializer(updated_assignment)
                    return Response({
                        'data': response_serializer.data,
                        'message': 'Assignment updated successfully'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'message': 'Validation error',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
        except Assignment.DoesNotExist:
            raise NotFound("Assignment not found")
        except Exception as e:
            return Response({
                'message': 'Failed to update assignment'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        summary="Delete assignment",
        description="Delete an existing assignment by its ID. Only teachers and admins can delete assignments.",
        tags=['Assignments']
    )
class AssignmentDeleteView(generics.DestroyAPIView):
    """API View to delete assignments"""
    permission_classes = [permissions.IsAuthenticated, TeacherPermission]
    queryset = Assignment.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                assignment = self.get_object()
                assignment.delete()
                return Response({
                    'message': 'Assignment deleted successfully'
                }, status=status.HTTP_200_OK)
        except Assignment.DoesNotExist:
            raise NotFound("Assignment not found")
        except Exception as e:
            return Response({
                'message': 'Failed to delete assignment'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def register_device_token(user, device_token):
    """
    Register a device token for the authenticated user.
    Allows multiple devices per user.
    """
    try:  
        if not device_token:
            return False

        # Check if user has existing devices
        existing_devices = CustomDevice.objects.filter(user=user, active=True)
        device_count = existing_devices.count()

        # If user has exactly one device, update its registration_id
        if device_count == 1:
            existing_device = existing_devices.first()
            existing_device.registration_id = device_token
            existing_device.save()
            return True

        # Otherwise, use the original get_or_create logic
        device, created = CustomDevice.objects.get_or_create(
            registration_id=device_token,
            defaults={
                'user': user,
                'active': True,
            }
        )
        
        if not created:
            # If device already exists, update user and set active
            device.user = user
            device.active = True
            device.save()

        return True
        
    except Exception as e:
        return False