from django.urls import  path
from . import views
urlpatterns = [
    path('showMessage/',views.ShowMsg().as_view()),
]
