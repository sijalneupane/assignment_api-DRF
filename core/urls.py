from django.urls import  path
from core import views as CoreViews
from assignments import views as AssignmentViews
# from rest_framework import routers
# router=routers.SimpleRouter()

urlpatterns = [
    path('createUser/',CoreViews.CrerateUser.as_view()),
    path('login/',CoreViews.LoginView.as_view()),
    path('addAssignment/',AssignmentViews.AddAssignmentView.as_view()),
    path('getAssignment/',AssignmentViews.GetAssignmentView.as_view()),
    path('getAssignment/<int:id>/',AssignmentViews.GetAssignmentByIdView.as_view()),
    path('editAssignment/<int:id>/',AssignmentViews.UpdateAssignmentView.as_view()),
    path('deleteAssignment/<int:id>/',AssignmentViews.DeleteAssignmentByIdView.as_view()),
    # path('showMessage/',CoreViews.ShowMsg().as_view()),
]
