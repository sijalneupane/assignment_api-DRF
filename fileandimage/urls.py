from django.urls import path
from .views import FileAndImageDeleteView, FileAndImageUpdateView, FileAndImageView,FileAndImageRetrieveView
urlpatterns = [
    path('upload',FileAndImageView.as_view(),name='fileandimage-upload'),
    path('list',FileAndImageRetrieveView.as_view(),name='fileandimage-list'),
    path('update/<str:pk>',FileAndImageUpdateView.as_view(),name='fileandimage-update'),
    path('delete/<str:pk>',FileAndImageDeleteView.as_view(),name='fileandimage-delete'),
]