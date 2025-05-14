from django.urls import  path
from . import views
urlpatterns = [
    path('createUser/',views.CrerateUser.as_view()),
    path('login/',views.LoginView.as_view()),
    path('addAssignment/',views.AddAssignmentView.as_view()),
    path('getAssignment/',views.GetAssignmentView.as_view()),
    path('getAssignment/<int:id>/',views.GetAssignmentByIdView.as_view()),
    path('editAssignment/<int:id>/',views.UpdateAssignmentView.as_view()),
    path('deleteAssignment/<int:id>/',views.DeleteAssignmentByIdView.as_view()),
    path('showMessage/',views.ShowMsg().as_view()),
]
