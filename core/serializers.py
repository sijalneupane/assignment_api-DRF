from rest_framework import serializers 
from rest_framework.exceptions import ValidationError
from .models import CustomUser, Assignment, Subject
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


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
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        return attrs

class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'deadline','teacher']
        
    def validate(self, attrs):
        # Ensure all required fields are present
        required_fields = ['title', 'description', 'subject', 'deadline']
        missing_fields = [field for field in required_fields if field not in attrs]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs

class SubjectNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class TeacherNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name']

class AssignmentSerializer(serializers.ModelSerializer):
    subject = SubjectNestedSerializer(read_only=True)
    teacher = TeacherNestedSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'teacher', 'deadline', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # These fields are read-only as they are auto-set

# class SubjectCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Subject
#         fields=['id','name','course_code','faculty','teached_by']
#         def validate(self,attrs):
#             required_fields=['name','course_code','faculty','teached_by']
#             missing_fields=[field for field in required_fields if field not in attrs]
#             if missing_fields:
#                 raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
#             return attrs
        
# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Subject
#         fields=['id','name','course_code','faculty','teached_by']
#         read_only_fields = ['id']  # This field is read-only as it is auto-generated

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(self, user):
        token = super().get_token(user)
           # Add custom claims here
        token['email'] = user.email
        token['role'] = user.role

        token['user_id'] = user.id
        return token