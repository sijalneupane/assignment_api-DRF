from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Subject

User = get_user_model()

class SubjectModelTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
    
    def test_subject_creation(self):
        subject = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
            description='Basic Mathematics',
            credits=3,
            created_by=self.admin_user
        )
        self.assertEqual(str(subject), 'MATH101 - Mathematics')
        self.assertEqual(subject.credits, 3)

class SubjectAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            role='admin'
        )
        self.student_user = User.objects.create_user(
            username='student',
            email='student@test.com',
            password='testpass123',
            role='student'
        )
        
        self.subject = Subject.objects.create(
            name='Mathematics',
            code='MATH101',
            description='Basic Mathematics',
            credits=3,
            created_by=self.admin_user
        )
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_list_subjects_authenticated(self):
        """Test that authenticated users can list subjects"""
        token = self.get_token_for_user(self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        response = self.client.get('/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
    
    def test_create_subject_admin_only(self):
        """Test that only admin can create subjects"""
        # Test with admin user
        token = self.get_token_for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {
            'name': 'Physics',
            'code': 'PHY101',
            'description': 'Basic Physics',
            'credits': 4
        }
        
        response = self.client.post('/subjects/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
    
    def test_create_subject_student_forbidden(self):
        """Test that student cannot create subjects"""
        token = self.get_token_for_user(self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        data = {
            'name': 'Physics',
            'code': 'PHY101',
            'description': 'Basic Physics',
            'credits': 4
        }
        
        response = self.client.post('/subjects/create/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
