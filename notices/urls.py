from django.urls import path
from .views import NoticeListCreateView, NoticeDetailView

urlpatterns = [
    path('', NoticeListCreateView.as_view(), name='notice-list-create'),
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]

# Alternative URL patterns if using separate views:
# urlpatterns = [
#     path('notices/create/', NoticeCreateView.as_view(), name='notice-create'),
#     path('notices/', NoticeListView.as_view(), name='notice-list'),
# ]