from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework.generics import CreateAPIView
# Create your views here.

class ShowMsg(APIView):
    def get(self, request):
        return Response(data={'message':'hellooo world !'})

class CrerateUser(CreateAPIView):
    model=CustomUser
    serializer_class=