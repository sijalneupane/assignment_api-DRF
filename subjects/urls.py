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
    path('<int:pk>', SubjectDetailView.as_view(), name='subject-detail'),
    path('update/<int:pk>', SubjectUpdateView.as_view(), name='subject-update'),
    path('delete/<int:pk>', SubjectDeleteView.as_view(), name='subject-delete'),
]
