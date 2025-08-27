from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Subject
from .serializers import SubjectSerializer, SubjectCreateUpdateSerializer
from utils.custompermissions import AdminOnlyPermission
from utils.customresponse import (
    GET_SuccessResponse, 
    POST_SuccessResponse, 
    PUTPATCH_SuccessResponse, 
    DELETE_SuccessResponse,
    BadRequestException,
    NotFoundException,
    InternalServerError
)
from drf_spectacular.utils import extend_schema, OpenApiExample

class SubjectListView(generics.ListAPIView):
    """
    List all subjects - accessible to all authenticated users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get all subjects",
        description="Retrieve all subjects. Accessible to all authenticated users.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Subjects retrieved successfully"},
                    "data": SubjectSerializer(many=True)
                }
            }
        },
        tags=['Subjects']
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return GET_SuccessResponse(
                data=serializer.data,
                message="Subjects retrieved successfully"
            )
        except Exception as e:
            return InternalServerError(
                message="Failed to retrieve subjects"
            )

class SubjectDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific subject - accessible to all authenticated users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get subject by ID",
        description="Retrieve a specific subject by its ID",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Subject retrieved successfully"},
                    "data": SubjectSerializer
                }
            },
            404: "Subject not found"
        },
        tags=['Subjects']
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return GET_SuccessResponse(
                data=serializer.data,
                message="Subject retrieved successfully"
            )
        except Subject.DoesNotExist:
            return NotFoundException(
                message="Subject not found"
            )
        except Exception as e:
            return InternalServerError(
                message="Failed to retrieve subject"
            )

class SubjectCreateView(generics.CreateAPIView):
    """
    Create a new subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOnlyPermission]

    @extend_schema(
        summary="Create new subject",
        description="Create a new subject. Only admin users can create subjects.",
        request=SubjectCreateUpdateSerializer,
        responses={
            201: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Subject created successfully"},
                    "data": SubjectSerializer
                }
            },
            400: "Validation errors",
            403: "Permission denied - Only admin can create subjects"
        },
        examples=[
            OpenApiExample(
                'Subject Creation Example',
                summary='Create subject request',
                description='Example request body for creating a new subject',
                value={
                    "name": "Computer Networks",
                    "code": "CN101",
                    "credit_hours": 3,
                    "semester": "Fifth Semester",
                    "faculty": "BCA"
                },
                request_only=True,
            )
        ],
        tags=['Subjects']
    )
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    subject = serializer.save(created_by=request.user)
                    response_serializer = SubjectSerializer(subject)
                    return POST_SuccessResponse(
                        data=response_serializer.data,
                        message="Subject created successfully"
                    )
                else:
                    return BadRequestException(
                        message="Validation error",
                        data=serializer.errors
                    )
        except Exception as e:
            return InternalServerError(
                message="Failed to create subject"
            )

class SubjectUpdateView(generics.UpdateAPIView):
    """
    Update a subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectCreateUpdateSerializer
    permission_classes = [IsAuthenticated, AdminOnlyPermission]

    @extend_schema(
        summary="Update subject",
        description="Update an existing subject. Only admin users can update subjects.",
        request=SubjectCreateUpdateSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Subject updated successfully"},
                    "data": SubjectSerializer
                }
            },
            400: "Validation errors",
            403: "Permission denied",
            404: "Subject not found"
        },
        examples=[
            OpenApiExample(
                'Subject Update Example',
                summary='Update subject request',
                description='Example request body for updating a subject',
                value={
                    "name": "Advanced Computer Networks",
                    "code": "ACN101",
                    "credit_hours": 4,
                    "semester": "Fifth Semester",
                    "faculty": "BCA"
                },
                request_only=True,
            )
        ],
        tags=['Subjects']
    )
    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    subject = serializer.save()
                    response_serializer = SubjectSerializer(subject)
                    return PUTPATCH_SuccessResponse(
                        data=response_serializer.data,
                        message="Subject updated successfully"
                    )
                else:
                    return BadRequestException(
                        message="Validation error",
                        data=serializer.errors
                    )
        except Subject.DoesNotExist:
            return NotFoundException(
                message="Subject not found"
            )
        except Exception as e:
            return InternalServerError(
                message="Failed to update subject"
            )

class SubjectDeleteView(generics.DestroyAPIView):
    """
    Delete a subject - only accessible to admin users
    """
    queryset = Subject.objects.all()
    permission_classes = [AdminOnlyPermission]

    @extend_schema(
        summary="Delete subject",
        description="Delete an existing subject by its ID. Only admin users can delete subjects.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Subject deleted successfully"}
                }
            },
            403: "Permission denied",
            404: "Subject not found"
        },
        tags=['Subjects']
    )
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.delete()
                return DELETE_SuccessResponse(
                    message="Subject deleted successfully"
                )
        except Subject.DoesNotExist:
            return NotFoundException(
                message="Subject not found"
            )
        except Exception as e:
            return InternalServerError(
                message="Failed to delete subject"
            )
