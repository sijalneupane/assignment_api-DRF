from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name', 'code', 'description', 'credits', 'created_at', 'updated_at']
        read_only_fields = ['subject_id', 'created_at', 'updated_at']

    def validate_code(self, value):
        """Validate that subject code is uppercase"""
        return value.upper()

class SubjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description', 'credits']

    def validate_code(self, value):
        """Validate that subject code is uppercase"""
        return value.upper()

    def validate_credits(self, value):
        """Validate that credits is between 1 and 10"""
        if value < 1 or value > 10:
            raise serializers.ValidationError("Credits must be between 1 and 10")
        return value
