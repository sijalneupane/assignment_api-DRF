
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Notices,TARGET_AUDIENCE_CHOICES

class NoticeWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating notices"""
    target_audience=serializers.JSONField(required=False)
    class Meta:
        model = Notices
        fields = ['title', 'notice_image_URL',
            'priority',
            'category',
            'target_audience']
    def validate_target_audience(self, value):
        # If empty or not provided, return default ['ALL']
        if not value:
            return ['ALL']
        
        # Validate all entries
        invalid = [v for v in value if v not in TARGET_AUDIENCE_CHOICES]
        if invalid:
            raise serializers.ValidationError(f"Invalid audience values: {invalid}")
        return value
    def validate(self, attrs):
        # Only validate fields that should be provided by user
        required_fields = ['title','notice_image_URL',]
        missing_fields = [field for field in required_fields if not attrs.get(field)]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs

class NoticeReadSerializer(serializers.ModelSerializer):
    """Serializer for reading notices with user details"""
    # issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    issued_by_username = serializers.CharField(source='issued_by.username', read_only=True)
    notice_image_URL = serializers.SerializerMethodField()
    target_audience = serializers.JSONField(required=False)
    class Meta:
        model = Notices
        fields = [
            'id', 'title','notice_image_URL',
            'issued_by',
            # 'issued_by_name',
            'issued_by_username',
            'priority',
            'category',
            'target_audience',
            'created_at', 'updated_at'
        ]
    def get_notice_image_URL(self, obj):
        url = str(obj.notice_image_URL) if obj.notice_image_URL else None
        if url.endswith('.jpg'): 
            url = url + '.jpg'
        if url.endswith('.png'):
            url = url + '.png'
        if url.endswith('.jpeg'):
            url = url + '.jpeg'
        return url if url else None
