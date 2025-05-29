from rest_framework import serializers 
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from core.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'name', 'gender', 'role', 'contact']
        extra_kwargs = {
            'password': {'write_only': True},
        #     'username': {'required': True},
        #     'email': {'required': True},
        #     'name': {'required': True},
        #     'gender': {'required': True},
        #     'role': {'required': True},
        #     'contact': {'required': True},
        }

    def validate(self, attrs):
        required_fields = ['username', 'email', 'name', 'gender', 'role', 'contact', 'password']
        missing_fields = [field for field in required_fields if field not in attrs or not attrs[field]]

        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    deviceToken = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password and device token are required.")

        return attrs

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
           # Add custom claims here
        token['email'] = user.email
        token['role'] = user.role

        token['user_id'] = user.id
        return token