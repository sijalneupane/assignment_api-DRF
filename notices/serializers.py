from rest_framework import serializers
from .models import Notices, TARGET_AUDIENCE_CHOICES
from fileandimage.models import FileAndImage
from core.models import CustomUser
from drf_spectacular.utils import extend_schema_field
from rest_framework.exceptions import ValidationError, NotFound


class FileAndImageMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAndImage
        fields = ["file_id", "file_url"]

class IssuedByMiniSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "name"]

    @extend_schema_field(serializers.CharField)
    def get_name(self, obj):
        # First try the name field, then fall back to username
        return obj.name if obj.name else obj.username


# ---------- CREATE SERIALIZER (all required) ----------
class NoticeCreateSerializer(serializers.ModelSerializer):
    target_audience = serializers.ListField(
        child=serializers.ChoiceField(choices=TARGET_AUDIENCE_CHOICES),
        required=True
    )
    file_id = serializers.CharField(required=True)
    issued_by = serializers.PrimaryKeyRelatedField(
        # queryset=CustomUser.objects.all(),
        required=False,
        read_only=True
    )

    class Meta:
        model = Notices
        fields = ["notice_id","title", "file_id", "priority", "category", "target_audience", "issued_by"]

    readonly_fields = ['notice_id']
    def validate_target_audience(self, value):
        if not value:
            raise serializers.ValidationError("target_audience is required")
        invalid = [v for v in value if v not in TARGET_AUDIENCE_CHOICES]
        if invalid:
            raise serializers.ValidationError(f"Invalid audience values: {invalid}")
        return value
    
    def validate_file_id(self, value):
        if value and not FileAndImage.objects.filter(file_id=value).exists():
            raise NotFound("File or Image does not exist with given file_id")
        return value

    def create(self, validated_data):
        file_id = validated_data.pop('file_id', None)
        notice = Notices(**validated_data)
        if file_id:
            try:
                file_image = FileAndImage.objects.get(file_id=file_id)
                notice.notice_image = file_image
            except FileAndImage.DoesNotExist:
                raise NotFound("File or Image does not exist with given file_id")
        notice.save()
        return notice
    # def validate_notice_image(self, value):
    #     if not value:
    #         raise serializers.ValidationError("notice_image is required")
    #     if not FileAndImage.objects.filter(pk=value).exists():
    #         raise NotFound("File or Image does not exist with given id ".format(value))
    #     return value


# ---------- UPDATE SERIALIZER (all optional) ----------
class NoticeUpdateSerializer(serializers.ModelSerializer):
    target_audience = serializers.ListField(
        child=serializers.ChoiceField(choices=TARGET_AUDIENCE_CHOICES),
        required=False
    )
    file_id = serializers.CharField(required=False)
    issued_by = serializers.PrimaryKeyRelatedField(
        # queryset=CustomUser.objects.all(),
        required=False,
        read_only=True
    )

    class Meta:
        model = Notices
        fields = ["notice_id","title", "file_id", "priority", "category", "target_audience", "issued_by"]

    readonly_fields = ['notice_id']
    def validate_target_audience(self, value):
        if value is None:
            return value
        if not isinstance(value, list):
            raise serializers.ValidationError("target_audience must be a list")
        invalid = [v for v in value if v not in TARGET_AUDIENCE_CHOICES]
        if invalid:
            raise serializers.ValidationError(f"Invalid audience values: {invalid}")
        return value
    
    def validate_file_id(self, value):
        if value and not FileAndImage.objects.filter(file_id=value).exists():
            raise NotFound("File or Image does not exist with given file_id")
        return value

    def update(self, instance, validated_data):
        file_id = validated_data.pop('file_id', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Handle file_id to notice_image mapping
        if file_id is not None:
            if file_id:  # If file_id is provided and not empty
                try:
                    file_image = FileAndImage.objects.get(file_id=file_id)
                    instance.notice_image = file_image
                except FileAndImage.DoesNotExist:
                    raise NotFound("File or Image does not exist with given file_id")
            else:  # If file_id is empty string, set notice_image to None
                instance.notice_image = None
        
        instance.save()
        return instance

# ---------- READ SERIALIZER ----------
class NoticeReadSerializer(serializers.ModelSerializer):
    issued_by = IssuedByMiniSerializer(read_only=True)
    notice_image = FileAndImageMiniSerializer(read_only=True)
    # file_id = serializers.SerializerMethodField()

    class Meta:
        model = Notices
        fields = [
            "notice_id", "title", "notice_image",
            "issued_by", "priority", "category",
            "target_audience", "created_at", "updated_at"
        ]

    @extend_schema_field(serializers.CharField)
    def get_file_id(self, obj):
        return obj.notice_image.file_id if obj.notice_image else None
