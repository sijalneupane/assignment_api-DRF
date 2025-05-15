from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from core.serializers import AssignmentCreateSerializer, AssignmentSerializer, CustomUserSerializer,LoginSerializer
# , SubjectCreateSerializer, SubjectSerializer
from .models import CustomUser,Assignment, Subject
from django.contrib.auth.hashers import check_password,make_password
# from rest_framework.generics import CreateAPIView
# Create your views here.

class ShowMsg(APIView):
    def get(self, request):
        return Response(data={'message':'hellooo world !'})

class CrerateUser(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # model=CustomUser
    # serializer_class=CustomUserSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = CustomUser.objects.get(email=email)
                if check_password(password, user.password):
                    # Use RefreshToken instead of AccessToken for better handling
                    # refresh = RefreshToken.for_user(user)
                    access=AccessToken.for_user(user)
                    
                    # Add custom claims to the token
                    # refresh['email'] = user.email
                    # refresh['role'] = user.role
                    access['email'] = user.email
                    access['role'] = user.role
                    
                    return Response({
                        # "refresh": str(refresh),
                        "token_access": str(access),
                        "message": "Login Success"
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            print("User is not authenticated , ${request.user.is_authenticated}")
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED) and False
        token = request.auth
        return token and token.get('role') in ['teacher', 'admin']
    
class AddAssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not TeacherPermission().has_permission(request, self):
            return Response({"error": "Only teachers and admins can add assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data['subject']=Subject.objects.get(name=data['subject_id']).id
        data['teacher'] = request.user.id
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
        
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAssignmentByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
    def put(self, request, id):
        if not TeacherPermission().has_permission(request, self):
            return Response({"error": "Only teachers and admins can update assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            data = request.data.copy()
            data['subject']=Subject.objects.get(name=data['subject']).id
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