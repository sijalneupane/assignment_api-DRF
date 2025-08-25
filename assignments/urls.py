from django.urls import path
from . import views as AssignmentViews
urlpatterns=[
     path('add', AssignmentViews.AddAssignmentView.as_view()),
    path('get', AssignmentViews.GetAssignmentView.as_view()),
    path('get/<int:id>', AssignmentViews.GetAssignmentByIdView.as_view()),
    path('edit/<int:id>', AssignmentViews.UpdateAssignmentView.as_view()),
    path('delete/<int:id>', AssignmentViews.DeleteAssignmentByIdView.as_view()),
]