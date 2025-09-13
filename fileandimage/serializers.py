from rest_framework import serializers
from .models import FileAndImage
from rest_framework.serializers import ImageField
from rest_framework.exceptions import ValidationError
from cloudinary.uploader import upload,destroy
from core.serializers import MiniUserSerializer
mime_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/webp', 'application/pdf']
class FileAndImageSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    file=serializers.FileField(required=True,write_only=True)
    class Meta:
        model=FileAndImage
        fields = [
            'file_id',
            'file_type',
            'meta_type',
            'file',        # input only
            'file_url',    # stored in DB
            'public_id',   # stored in DB
            'user',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'file_id',
            'created_at',
            'updated_at',
            'user',
            'meta_type',
            'file_url',
            'public_id'
        ]

        extra_kwargs = {
            'file_type': {'required': True},
            'file': {'required': True, 'write_only': True},
        }
    def validate(self, attrs):
        file = attrs.get('file')
        file_type = attrs.get('file_type')

        if not file:
            raise ValidationError({"message": "file field is required."})
        if file.content_type not in mime_types:
            raise ValidationError({"message": "Invalid file type. "})
        if not file_type:
            raise ValidationError({"message": "file_type field is required."})
        if file_type not in ['profile', 'assignment', 'notice']:
            raise ValidationError({"message": "Invalid file_type. Must be 'profile', 'document', or 'other'."})
        if file.size > 2 * 1024 * 1024:
            raise ValidationError({"message": "File size should not exceed 2MB."})
     
        image_mime_types = [mime for mime in mime_types if mime.startswith('image/')]
        pdf_mime_type = 'application/pdf'

        # Validation rules
        if file_type == 'profile':
            if file.content_type not in image_mime_types:
                raise ValidationError({"message": "Profile files must be an image."})

        elif file_type == 'assignment':
            if file.content_type != pdf_mime_type:
                raise ValidationError({"message": "Assignment files must be a PDF."})
        attrs['meta_type'] = file.content_type.split('/')[-1]  # Extracting the subtype as meta_type
        return attrs

    def create(self, validated_data):
        try:
            file = validated_data.pop('file')   # remove temporary upload field
            upload_res = upload(file, folder="assignment_api")

            validated_data['file_url'] = upload_res['secure_url']
            validated_data['public_id'] = upload_res['public_id']

            return FileAndImage.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError({"message": "File upload failed.", "error": str(e)})

    def update(self, instance, validated_data):
        try:
            file = validated_data.pop('file', None)

            if file:
                # Delete old file from Cloudinary
                destroy(instance.public_id)

                upload_res = upload(file)
                instance.meta_type = upload_res['format']
                instance.public_id = upload_res['public_id']
                instance.file_url = upload_res['secure_url']

            for attr, value in validated_data.items():
                setattr(instance, attr, value)

            instance.save()
            return instance
        except Exception as e:
            raise ValidationError({"message": "File update failed.", "error": str(e)})
    
