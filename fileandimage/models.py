from django.db import models
from cloudinary.models import CloudinaryField
from shortuuidfield import ShortUUIDField
from core.models import CustomUser
# from enum import Enum
# Create your models here.

class FileType(models.TextChoices):
    PROFILE = 'profile', 'Profile'
    NOTICE = 'notice', 'Notice'
    ASSIGNMENT = 'assignment', 'Assignment'
fileType=[ 
        ('profile','Profile'), 
        ('notice','Notice'), 
        ('assignment','Assignment'), 
    ]

# class fileType(Enum):
#     PROFILE = 'profile'
#     NOTICE = 'notice'
#     ASSIGNMENT = 'assignment'
    
    
    
class FileMetaType(models.TextChoices):
    JPG = 'jpg', 'JPG'
    PNG = 'png', 'PNG'
    JPEG = 'jpeg', 'JPEG'
    GIF = 'gif', 'GIF'
    WEBP = 'webp', 'WEBP'
    PDF = 'pdf', 'PDF' 
# fileMetaType=[
#     ('jpg','JPG'),
#     ('png','PNG'),
#     ('jpeg','JPEG'),
#     ('gif','GIF'),
#     ('webp','WEBP'),
#     ('pdf','PDF'),
# ]
# class fileMetaType(Enum):
#     JPG = 'jpg'
#     PNG = 'png'
#     JPEG = 'jpeg'
#     GIF = 'gif'
#     WEBP = 'webp'
#     PDF = 'pdf'

class FileAndImage(models.Model):
    file_id=ShortUUIDField(primary_key=True,max_length=6)
    file_url=models.CharField(max_length=255,null=False,blank=False) 
    public_id=models.CharField(max_length=255,null=False,blank=False)
    file_type=models.CharField(null=False,blank=False,max_length=15,choices=FileType.choices)
    meta_type=models.CharField(null=False,blank=False,max_length=15,choices=FileMetaType.choices)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='files')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"FileAndImage {self.file_id}"