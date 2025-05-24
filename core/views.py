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

from assignments.views import register_device_token

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
    def post(self, request) :
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            device_token=serializer.validated_data["deviceToken"]
            try:
                user = CustomUser.objects.get(email=email)
                if check_password(password, user.password):
                    # Use RefreshToken instead of AccessToken for better handling
                    # refresh = RefreshToken.for_user(user)
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
                        "role":access.get('role')
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            # except Exception as e:
            #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   