from django.urls import  path
from . import views
urlpatterns = [
    path('createUser/',views.CrerateUser.as_view()),
    path('login/',views.LoginView.as_view()),
    path('addAssignment/',views.AssignmentView.as_view()),
    path('showMessage/',views.ShowMsg().as_view()),
]
