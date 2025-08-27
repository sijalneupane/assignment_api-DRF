
from .models import CustomUser, Assignment, Subject
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from subjects.serializers import SubjectSerializer
class AssignmentCreateSerializer(serializers.ModelSerializer):
    subject_id = serializers.CharField(write_only=True)  # Accept subject_id in request
    
    class Meta:
        model = Assignment
        fields = ['assignment_id', 'title', 'description', 'subject_id', 'deadline','semester','faculty']

    def validate(self, attrs):
        # Ensure all required fields are present
        required_fields = ['title', 'description', 'subject_id','semester','faculty']
        missing_fields = [field for field in required_fields if field not in attrs]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs
    
    def create(self, validated_data):
        subject_id = validated_data.pop('subject_id')
        try:
            subject = Subject.objects.get(subject_id=subject_id)
        except Subject.DoesNotExist:
           raise NotFound(f"Subject with id '{subject_id}' does not exist.") 

        validated_data['subject'] = subject
        return super().create(validated_data)



class AssignmentSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)  # Nested subject details

    class Meta:
        model = Assignment
        fields = ['assignment_id', 'title', 'description', 'subject', 'teacher', 'deadline','faculty','semester']
        # read_only_fields = ['created_at', 'updated_at']  # These fields are read-only as they are auto-set
