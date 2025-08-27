from django.urls import path
from .views import (
    NoticeCreateView,
    NoticeListView,
    NoticeDetailView,
    NoticeUpdateView,
    NoticeDeleteView
)

urlpatterns = [
    path('list', NoticeListView.as_view(), name='notice-list'),
    path('create', NoticeCreateView.as_view(), name='notice-create'),
    path('<str:pk>', NoticeDetailView.as_view(), name='notice-detail'),
    path('update/<str:pk>', NoticeUpdateView.as_view(), name='notice-update'),
    path('delete/<str:pk>', NoticeDeleteView.as_view(), name='notice-delete'),
]