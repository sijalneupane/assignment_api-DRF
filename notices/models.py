from django.db import models
from core.models import CustomUser

TARGET_AUDIENCE_CHOICES=['ALL','BCA','BIM','CSIT']
# Create your models here.
class Notices(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    CATEGORY_CHOICES = [
        ('exam', 'Exam'),
        ('holiday', 'Holiday'),
        ('general', 'General'),
        ('seminar', 'Seminar'),
    ]
    title=models.CharField(max_length=200)
    content=models.TextField()
    issued_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']}, default=1)
    notice_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    target_audience = models.JSONField(default=list, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title