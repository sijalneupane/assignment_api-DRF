from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # 🔑 Set role to admin

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role=admin')
        return self.create_user(username, email, password, **extra_fields)

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (('student','Student'), ('admin','Admin'), ('teacher','Teacher'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # fix reverse accessor clash if needed (you already have)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()  # ✅ Use your custom manager

    def __str__(self):
        return self.username

class Subject(models.Model):
    FACULTY_CHOICES=[('bca','BCA'),('bim','BIM'),('csit','CSIT')]
    name = models.CharField(max_length=250)
    course_code = models.CharField(max_length=250)
    faculty=models.CharField(max_length=10, choices=FACULTY_CHOICES)
    teached_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role__in': ['admin', 'teacher']}, default=1)

    def __str__(self):
        return self.name
    
class Assignment(models.Model):
    title=models.CharField(max_length=250)
    description=models.TextField()
    deadline=models.DateTimeField()

    def __str__(self):
        return self.title