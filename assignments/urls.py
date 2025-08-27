from django.urls import path
from .views import (
    AssignmentCreateView,
    AssignmentListView,
    AssignmentDetailView,
    AssignmentUpdateView,
    AssignmentDeleteView
)

urlpatterns = [
    path('create', AssignmentCreateView.as_view(), name='assignment-create'),
    path('list', AssignmentListView.as_view(), name='assignment-list'),
    path('<str:pk>', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('update/<str:pk>', AssignmentUpdateView.as_view(), name='assignment-update'),
    path('delete/<str:pk>', AssignmentDeleteView.as_view(), name='assignment-delete'),
]