
from .models import CustomUser, Assignment, Subject
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
class AssignmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'deadline','teacher','semester','faculty']
        
    def validate(self, attrs):
        # Ensure all required fields are present
        required_fields = ['title', 'description', 'subject','semester','faculty']
        missing_fields = [field for field in required_fields if field not in attrs]
        
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
        
        return attrs



class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'teacher', 'deadline','faculty','semester']
        # read_only_fields = ['created_at', 'updated_at']  # These fields are read-only as they are auto-set


# class SubjectCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Subject
#         fields=['id','name','course_code','faculty','teached_by']
#         def validate(self,attrs):
#             required_fields=['name','course_code','faculty','teached_by']
#             missing_fields=[field for field in required_fields if field not in attrs]
#             if missing_fields:
#                 raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")
#             return attrs
        
# class SubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Subject
#         fields=['id','name','course_code','faculty','teached_by']
#         read_only_fields = ['id']  # This field is read-only as it is auto-generated

