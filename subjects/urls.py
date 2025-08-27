from django.urls import path
from .views import (
    SubjectListView,
    SubjectDetailView,
    SubjectCreateView,
    SubjectUpdateView,
    SubjectDeleteView
)

urlpatterns = [
    path('list', SubjectListView.as_view(), name='subject-list'),
    path('create', SubjectCreateView.as_view(), name='subject-create'),
    path('<str:pk>', SubjectDetailView.as_view(), name='subject-detail'),
    path('update/<str:pk>', SubjectUpdateView.as_view(), name='subject-update'),
    path('delete/<str:pk>', SubjectDeleteView.as_view(), name='subject-delete'),
]
