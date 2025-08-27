from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from core.serializers import  CustomUserSerializer,LoginSerializer
# , SubjectCreateSerializer, SubjectSerializer
from .models import CustomUser
from django.contrib.auth.hashers import check_password,make_password
# from rest_framework.generics import CreateAPIView
# Create your views here.
from drf_spectacular.utils import extend_schema, OpenApiExample
from assignments.views import register_device_token
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Show success message as Health Check",
    description="Returns a simple success message. Main API endpoint for health check.",
    responses={
        200: {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "example": True
                },
                "message": {
                    "type": "string",
                    "example": "success"
                }
            }
        }
    },
    tags=["App Health"],
)
class ShowMsg(APIView):
    def get(self, request):
        # return BadRequestException("success",{"name":"John Doe"})
        return Response({
            'success': True,
            'message': 'success'
        }, status=status.HTTP_200_OK)

class CrerateUser(APIView):
    @extend_schema(
        tags=['Authentication'],
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
                    },
                    "success": {
                        "type": "boolean",
                        "example": True
                    },
                    "data":{
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "integer",
                                "example": 1
                            },
                            "username": {
                                "type": "string",
                                "example": "bioExplorer"
                            },
                            "email": {
                                "type": "string",
                                "example": "science.queen@outlook.com"
                            },
                            "name": {
                                "type": "string",
                                "example": "Dr. Ellen Wright"
                            },
                            "gender": {
                                "type": "string",
                                "example": "female"
                            },
                            "role": {
                                "type": "string",
                                "example": "teacher"
                            },
                            "contact": {
                                "type": "string",
                                "example": "6429183750"
                            }
                        }
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "success": {
                        "type": "boolean",
                        "example": False
                    },
                    "message": {
                        "type": "string",
                        "example": "Validation errors"
                    },
                    "data": {
                        "type": "object",
                        "example": { 
                            'email': ['This field is required.'], 
                            'password': ['This field is required.'] 
                            }
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
            return Response({
                'message': 'User registered successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Failed to create new user',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

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
                        'message': 'Login Success',
                        'data': {
                            'token': str(access),
                            'user': CustomUserSerializer(user).data
                        }
                    }, status=status.HTTP_200_OK)
                # return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
                raise AuthenticationFailed("Invalid password")
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Email not found")
            except Exception as e:
                return Response({
                    'message': 'Failed',
                    'error': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'message': 'Failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

