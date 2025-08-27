from django.db import models
from core.models import CustomUser
from fcm_django.models import AbstractFCMDevice
from django.utils import timezone
import datetime
from subjects.models import Subject 
from shortuuidfield import ShortUUIDField

class CustomDevice(AbstractFCMDevice):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


# class Subject(models.Model):
#     FACULTY_CHOICES=[('bca','BCA'),('bim','BIM'),('csit','CSIT')]
#     name = models.CharField(max_length=250)
#     course_code = models.CharField(max_length=250)
#     faculty=models.CharField(max_length=10, choices=FACULTY_CHOICES)
#     teached_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']}, default=1)

#     def __str__(self):
#         return self.name
    
class Assignment(models.Model):
    # -- indicates value or field added for making assignment app in college[flutter class] for others to use also
    # --
    FACULTY_CHOICES=[("BCA","BCA"),("BIM","BIM"),("CSIT","CSIT")]
    SEMESTER_CHOICES = [
    ("First Semester", "First Semester"),
    ("Second Semester", "Second Semester"),
    ("Third Semester", "Third Semester"),
    ("Fourth Semester", "Fourth Semester"),
    ("Fifth Semester", "Fifth Semester"),
    ("Sixth Semester", "Sixth Semester"),
    ("Seventh Semester", "Seventh Semester"),
    ("Eighth Semester", "Eighth Semester"),
]
    assignment_id = ShortUUIDField(max_length=6, primary_key=True)
    title=models.CharField(max_length=250)
    description=models.TextField()
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE, blank=False,null=False)
    teacher=models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']}, default=0)
    deadline = models.DateTimeField(default= timezone.now() + datetime.timedelta(days=7))
    #--
    semester=models.CharField(max_length=20, choices=SEMESTER_CHOICES,default="No Semester")
    faculty=models.CharField(max_length=20, choices=FACULTY_CHOICES,default="No faculty")
    ##end of -- field
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title