from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,UpdateAPIView,DestroyAPIView,ListAPIView
from .models import FileAndImage
from .serializers import FileAndImageSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser,MultiPartParser
from cloudinary.uploader import destroy
from rest_framework.exceptions import ValidationError
from utils.customresponse import POST_SuccessResponse, GET_SuccessResponse,PUTPATCH_SuccessResponse
from utils.pagination_class import CustomPagination
# Create your views here.
@extend_schema(
    summary="Upload a file or image",
    description="Upload a file or image associated with the authenticated user.",
    request=FileAndImageSerializer,
    tags=['FileAndImage']
)
class FileAndImageView(CreateAPIView):
    queryset = FileAndImage.objects.all()
    serializer_class = FileAndImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return POST_SuccessResponse(data=response.data, message="File uploaded successfully.")
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


        
@extend_schema(
    summary="Update a file and image with file_id",
    description="Update a file and image associated with the authenticated user.",
    request=FileAndImageSerializer,
    tags=['FileAndImage']
)
class FileAndImageUpdateView(UpdateAPIView):
    queryset = FileAndImage.objects.all()
    serializer_class=FileAndImageSerializer
    permission_classes=[IsAuthenticated]
    parser_classes=(MultiPartParser,FormParser)
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return PUTPATCH_SuccessResponse(data=response.data, message="File updated successfully.")

    def perform_update(self, serializer):
        # user = self.request.user
        serializer.save()  # You can pass additional fields here if needed



@extend_schema(
    summary="Retrieve a file and image",
    description="Retrieve a file and image associated with the authenticated user.",
    tags=['FileAndImage'],
)
class FileAndImageRetrieveView(ListAPIView):
    queryset = FileAndImage.objects.all()
    serializer_class = FileAndImageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return FileAndImage.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Call the pagination class method directly with the message parameter
            return self.paginator.get_paginated_response(serializer.data, 'Notices retrieved successfully')
        
        # Fallback if pagination is not used
        serializer = self.get_serializer(queryset, many=True)
        return GET_SuccessResponse(data=serializer.data, message="Files retrieved successfully.")



@extend_schema(
    summary="Delete a file and image",
    description="Delete a file and image associated with the authenticated user.",
    tags=['FileAndImage']
)
class FileAndImageDeleteView(DestroyAPIView):
    queryset = FileAndImage.objects.all()
    serializer_class=FileAndImageSerializer
    permission_classes=[IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # Delete file from Cloudinary
            destroyed = destroy(instance.public_id)
            # Delete instance from database
            instance.delete()
            return Response({
                "message": "File deleted successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError({"message": "File deletion failed.", "error": str(e)})