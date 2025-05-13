from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import AccessToken
from core.serializers import AssignmentCreateSerializer, AssignmentSerializer, CustomUserSerializer,LoginSerializer
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
                    token = AccessToken()
                    token['id'] = user.id
                    token['email'] = user.email
                    token['role'] = user.role
                    return Response({"token": str(token), "message": "Login Success"}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeacherPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED) and False
        token = request.auth
        return token and token.get('role') in ['teacher', 'admin']
    
class AssignmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if not TeacherPermission().has_permission(request, self):
            return Response({"error": "Only teachers and admins can add assignments"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()
        data['subject']=Subject.objects.get(name=data['subject']).id
        data['teacher'] = request.user.id
        serializer = AssignmentCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Assignment added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)