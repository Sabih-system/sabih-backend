from django.urls import path
from .views import *

urlpatterns = [
    path('create_employee/', EmployeeCreationView.as_view(), name='create_employee'),
    path("create_task/", TaskCreationView.as_view(), name="create_task"),
    path("get_employee_tasks/", GetEmployeeTasks.as_view(), name="get_employee_tasks"),
    path("update_task/<uuid:pk>/", UpdateTask.as_view(), name="update_task"),
]