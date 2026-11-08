from django.urls import path
from .views import CustomerListCreateView, TaskListCreateView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
]