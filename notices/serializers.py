
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Notices,TARGET_AUDIENCE_CHOICES

class NoticeWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating notices"""
    target_audience=serializers.JSONField(required=False)
    class Meta:
        model = Notices
        fields = ['title', 'content', 'notice_date',
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
        required_fields = ['title', 'content', 'notice_date']
        missing_fields = [field for field in required_fields if not attrs.get(field)]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs

class NoticeReadSerializer(serializers.ModelSerializer):
    """Serializer for reading notices with user details"""
    # issued_by_name = serializers.CharField(source='issued_by.get_full_name', read_only=True)
    issued_by_username = serializers.CharField(source='issued_by.username', read_only=True)
    
    target_audience = serializers.JSONField(required=False)
    class Meta:
        model = Notices
        fields = [
            'id', 'title', 'content', 'notice_date', 
            'issued_by',
            # 'issued_by_name',
            'issued_by_username',
            'priority',
            'category',
            'target_audience',
            'created_at', 'updated_at'
        ]