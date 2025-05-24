
from assignments.models import CustomDevice
from rest_framework import status,permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Assignment,Subject
from core.models import CustomUser
from .serializers import AssignmentCreateSerializer,AssignmentSerializer
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
# Create your views here.
# Initialize Firebase app (ensure this runs only once)
# if not firebase_admin._apps:
#     cred = credentials.Certificate('path/to/your/firebase/credentials.json')
#     firebase_admin.initialize_app(cred)

# def send_firebase_notification_to_topic(topic, title, body, data_payload=None):
#     """
#     Send a Firebase notification to all devices subscribed to a topic using django-fcm.
#     """
#     if not topic or not title or not body:
#         raise ValueError("Missing required fields: topic, title, or body.")

#     devices = CustomDevice.objects.filter(active=True, type='android', user__groups__name=topic)
#     # Adjust the filter as per your topic subscription logic

#     result = devices.send_message(
#         title=title,
#         body=body,
#         data=data_payload or {},
#     )
#     return result

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
def register_device_token( user, device_token):
    """
    Register a device token for the authenticated user.
    Allows multiple devices per user.
    """
    # # Explicitly set renderer classes if needed
    # request.accepted_renderer = JSONRenderer()
    """
    Register a device token for the authenticated user.
    Allows multiple devices per user.
    """
    # device_token = data.get('deviceToken')
    # device_type = request.data.get('deviceType', 'android')  # default to android
    try:  
        if not device_token:
            return Response({'error': 'Device token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        device, created = CustomDevice.objects.get_or_create(
            registration_id=device_token,
            defaults={
                'user': user,
                # 'type': device_type,
                'active': True,
            }
        )
        if not created:
            # If device already exists, update user and set active
            device.user = user
            # device.type = device_type
            device.active = True
            device.save()

        return True
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
class TeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            print("User is not authenticated , ${request.user.is_authenticated}")
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED) and False
        token = request.auth
        return token and token.get('role') in ['teacher', 'admin']
    
class AddAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Create new assignment",
        description="Add a new assignment. Only teachers and admins can create assignments.",
        request=AssignmentCreateSerializer,
        responses={
            201: AssignmentSerializer,
            400: "Validation errors",
            403: "Permission denied - Only teachers and admins can add assignments",
            404: "Subject or teacher not found"
        },
        examples=[
            OpenApiExample(
                'Assignment Creation Example',
                summary='Create assignment request',
                description='Example request body for creating a new assignment',
                value={
                    "title": "Computer Network",
                    "description": "Complete exercises 1-10 from chapter 3. Show all your work.",
                    "subjectName": "Computer Network",
                    "semester":"First Semester",
                    "faculty":"BCA"
                },
                request_only=True,
            )
        ],
        tags=['Assignments']
    )
    def post(self, request):
        if not TeacherPermission().has_permission(request, self):
            return Response({"error": "Only teachers and admins can add assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        try:
            data['subject']=Subject.objects.get(name=data['subjectName']).id
        except Subject.DoesNotExist:
            return Response({"error":"SUbject does not exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            data['teacher'] = request.user.id
        except CustomUser.DoesNotExist:
            return Response({"error":"Teacher does not exist"},status=status.HTTP_404_NOT_FOUND)
        serializer = AssignmentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Assignment added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        assignments = Assignment.objects.all().order_by("id")
        serializer = AssignmentSerializer(assignments, many=True)
        data = []
        for assignment, assignment_data in zip(assignments, serializer.data):
            try:
                subject = Subject.objects.get(id=assignment.subject.id)
            except Subject.DoesNotExist:
                return Response({"error": "Subject Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                teacher = CustomUser.objects.get(id=assignment.teacher.id)
            except CustomUser.DoesNotExist:
                return Response({"error": "Teacher Does Not Exist"}, status=status.HTTP_404_NOT_FOUND)
            assignment_data = dict(assignment_data)
            assignment_data['subjectName'] = subject.name
            assignment_data['teacher'] = teacher.name
            data.append(assignment_data)
        return Response(data, status=status.HTTP_200_OK)

class GetAssignmentByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Get assignment by ID",
        description="Retrieve a specific assignment by its ID with subject and teacher details",
        responses={
            200: AssignmentSerializer,
            401: "Authentication required",
            404: "Assignment, subject, or teacher not found"
        },
        parameters=[
            OpenApiParameter(
                name='id',
                description='Assignment ID',
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            ),
        ],
        tags=['Assignments']
    )
    def get(self, request, id):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # try:
        assignment = Assignment.objects.get(id=id)
        subject = Subject.objects.get(id=assignment.subject_id.id)
        teacher = CustomUser.objects.get(id=assignment.teacher_id.id)
        serializer = AssignmentSerializer(assignment)
        data = serializer.data
        data['subject'] = subject.name
        data['teacher'] = teacher.name  # or teacher.name if you prefer
        return Response(data, status=status.HTTP_200_OK)
        # except Assignment.DoesNotExist:
        #     return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        # except Subject.DoesNotExist:
        #     return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
        # except CustomUser.DoesNotExist:
        #     return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UpdateAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @extend_schema(
        summary="Update assignment",
        description="Update an existing assignment. Only teachers and admins can update assignments.",
        request=AssignmentCreateSerializer,
        responses={
            200: AssignmentSerializer,
            400: "Validation errors",
            403: "Permission denied - Only teachers and admins can update assignments",
            404: "Assignment, subject, or teacher not found"
        },
        parameters=[
            OpenApiParameter(
                name='id',
                description='Assignment ID to update',
                required=True,
                type=int,
                location=OpenApiParameter.PATH
            ),
        ],
        examples=[
            OpenApiExample(
                'Assignment Update Example',
                summary='Update assignment request',
                description='Example request body for updating an assignment',
                value={
                    "title": "Computer Network",
                    "description": "Complete exercises 1-10 from chapter 3. Show all your work.",
                    "subjectName": "Computer Network",
                    "semester":"First Semester",
                    "faculty":"BCA"
                },
                request_only=True,
            )
        ],
        tags=['Assignments']
    )
    def put(self, request, id):
        if not TeacherPermission().has_permission(request, self): 
            return Response({"error": "Only teachers and admins can update assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data.copy()
            data['subject']=Subject.objects.get(name=data['subjectName']).id
            data['teacher'] = request.user.id
            assignment = Assignment.objects.get(id=id)
            serializer = AssignmentCreateSerializer(assignment, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Assignment updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Assignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({"error": "Teacher or admin not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteAssignmentByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, id):
        if not TeacherPermission().has_permission(request, self):
            return Response({"error": "Only teachers and admins can delete assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            assignment = Assignment.objects.get(id=id)
            assignment.delete()
            return Response({"message": "Assignment deleted successfully"}, status=status.HTTP_200_OK)
        except Assignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        
# class SubjectCreateView(APIView):
#     permission_classes=[permissions.IsAuthenticated]
#     def post(self,request):
#         if not TeacherPermission().has_permission(request, self):
#             return Response({"error": "Only teachers and admins can delete assignments"}, status=status.HTTP_403_FORBIDDEN)
        
#         data=request.data.copy()
#         data['teached_by']=CustomUser.objects.get(name=data['teached_by']).id
#         serializer=SubjectCreateSerializer(data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message":"Subject Added Successfully"},status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GetSubjectView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         assignments = Assignment.objects.all()
#         serializer = AssignmentSerializer(assignments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class GetSubjectByIdView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, id):
#         if not request.user.is_authenticated:
#             return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
#         try:
#             subject = Subject.objects.get(id=id)
#             serializer = SubjectSerializer(subject)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Subject.DoesNotExist:
#             return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)
        
# class UpdateSubjectView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def put(self, request, id):
#         if not TeacherPermission().has_permission(request, self):
#             return Response({"error": "Only teachers and admins can update Subject"}, status=status.HTTP_403_FORBIDDEN)
        
#         try:
#             data = request.data.copy()
#             data['subject']=Subject.objects.get(name=data['subject']).id
#             data['teacher'] = request.user.id
#             assignment = Assignment.objects.get(id=id)
#             serializer = AssignmentCreateSerializer(assignment, data=data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({"message": "Assignment updated successfully"}, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Assignment.DoesNotExist:
#             return Response({"error": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        
# class DeleteSubjectByIdView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def delete(self, request, id):
#         if not TeacherPermission().has_permission(request, self):
#             return Response({"error": "Only teachers and admins can delete Subject"}, status=status.HTTP_403_FORBIDDEN)
        
#         try:
#             assignment = Assignment.objects.get(id=id)
#             assignment.delete()
#             return Response({"message": "Subject deleted successfully"}, status=status.HTTP_200_OK)
#         except Assignment.DoesNotExist:
#             return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)