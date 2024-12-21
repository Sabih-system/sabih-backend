from django.urls import path
from .views import *

urlpatterns = [
    path('create_employee/', EmployeeCreationView.as_view(), name='create_employee'),
]