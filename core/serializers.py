from rest_framework.serializers import Serializer
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(Serializer.model):
# class AssignmentSerializer(Serializer.model):
#     model=models.Assignment


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(self,user):
        token = super().get_token(user)
           # Add custom claims here
        token['email'] = user.email
        token['role'] = user.role

        token['user_id'] = user.id
        return token