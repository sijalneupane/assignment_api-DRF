
from .models import CustomUser, Assignment, Subject
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

class MinimalSubjectSerializer(serializers.ModelSerializer):
    """Minimal subject serializer that only returns id and name"""
    class Meta:
        model = Subject
        fields = ['subject_id', 'name']
class AssignmentCreateSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(write_only=True)  # Accept subject_name in request
    
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'title', 'description', 'subject_name', 'deadline','semester','faculty']

    def validate(self, attrs):
        # Ensure all required fields are present
        required_fields = ['title', 'description', 'subject_name','semester','faculty']
        missing_fields = [field for field in required_fields if field not in attrs]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs
    
    def create(self, validated_data):
        subject_name = validated_data.pop('subject_name')
        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            raise NotFound(f"Subject with name '{subject_name}' does not exist.")
        validated_data['subject'] = subject
        return super().create(validated_data)



class AssignmentSerializer(serializers.ModelSerializer):
    subject = MinimalSubjectSerializer(read_only=True)  # Only subject id and name

    class Meta:
        model = Assignment
        fields = ['assignment_id', 'title', 'description', 'subject', 'teacher', 'deadline','faculty','semester']
        # read_only_fields = ['created_at', 'updated_at']  # These fields are read-only as they are auto-set
