#from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Customer, Task
from .serializers import CustomerSerializer, TaskSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer