from django.urls import path
from core import views as CoreViews

urlpatterns = [
    path('health', CoreViews.ShowMsg().as_view()),
    path('createUser', CoreViews.CrerateUser.as_view()),
    path('login', CoreViews.LoginView.as_view()),
    path('test-custom-response', CoreViews.TestCustomResponse.as_view()),
]
