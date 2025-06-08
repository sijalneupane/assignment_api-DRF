from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from core.serializers import  CustomUserSerializer,LoginSerializer
# , SubjectCreateSerializer, SubjectSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password,make_password
# from rest_framework.generics import CreateAPIView
# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiExample
from assignments.views import register_device_token

class ShowMsg(APIView):
    def get(self, request):
        return Response(data={'message':'hellooo world !'})

class CrerateUser(APIView):
    @extend_schema(
        summary="Register new user",
        description="Create a new user account with the provided information",
        request=CustomUserSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "User registered successfully"
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Validation errors"
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                'Create User Example',
                summary='Create a new user',
                description='Example request body for user creation',
                value={
                    "email": "science.queen@outlook.com",
                    "username": "bioExplorer",
                    "password": "m1toch0ndria!",
                    "name": "Dr. Ellen Wright",
                    "gender": "female",
                    "role": "teacher",
                    "contact": "6429183750"
                }, # Adjust fields based on your CustomUserSerializer
                request_only=True,
            )
        ],
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # model=CustomUser
    # serializer_class=CustomUserSerializer

class LoginView(APIView):
    @extend_schema(
        summary="User login",
        description="Authenticate user and return access token",
        request=LoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    },
                    "message": {
                        "type": "string",
                        "example": "Login Success"
                    },
                    "role": {
                        "type": "string",
                        "example": "student"
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Validation errors"
                    }
                }
            },
            401: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid password"
                    }
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "User not found"
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                'Login Example',
                summary='User login request',
                description='Example request body for user login',
                value={
                    'email': 'user@example.com',
                    'password': 'securePassword123',
                    'deviceToken': 'device_fcm_token_here'
                },
                request_only=True,
            )
        ],
        tags=['Authentication']
    )
    def post(self, request) :
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            device_token = request.data.get('deviceToken', None)
            try:
                user = CustomUser.objects.get(email=email)
                if check_password(password, user.password):
                    # Use RefreshToken instead of AccessToken for better handling
                    # refresh = RefreshToken.for_user(user)
                    if device_token:
                         if not register_device_token(user, device_token):
                            raise Exception("Failed to register device")
                    access=AccessToken.for_user(user)
                    
                    # Add custom claims to the token
                    # refresh['email'] = user.email
                    # refresh['role'] = user.role
                    access['email'] = user.email
                    access['role'] = user.role
                    
                    return Response({
                        # "refresh": str(refresh),
                        "token": str(access),
                        "message": "Login Success",
                        "id":access.get('user_id'),
                        "role":access.get('role'),
                        "email": access.get('email'),
                        "username": user.username,
                        "name": user.name,
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   