from django.utils import timezone
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
@extend_schema(
        tags=['Authentication'],
        summary="Register new user",
        description="Create a new user account with the provided information",
        request=CustomUserSerializer,
)
class CreateUser(APIView):
    serializer_class=CustomUserSerializer
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

@extend_schema(
    summary="User login",
    description="Authenticate user and return access token",
    request=LoginSerializer,
    tags=['Authentication']
)
class LoginView(APIView):
    serializer_class = LoginSerializer
    def post(self, request) :
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            device_token = request.data.get('deviceToken', None)
            try:
                user = CustomUser.objects.get(email=email)
                if check_password(password, user.password):
                    user.last_login = timezone.now()
                    user.save()
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
                else :
                    return Response({"message": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED,)
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed({"message": "Email not found"})
            except Exception as e:
                return Response({
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

