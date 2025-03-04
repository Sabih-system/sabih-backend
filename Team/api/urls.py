from django.urls import path
from .views import *

urlpatterns = [
    path('create_employee/', EmployeeCreationView.as_view(), name='create_employee'),
    path("create_task/", TaskCreationView.as_view(), name="create_task"),
    path("employee_tasks/", GetEmployeeTasks.as_view(), name="get_employee_tasks"),
    path('employee_list/', EmployeeList.as_view(), name='get_employee_list'),
    path('employee_detail/<uuid:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
    path("update_task/<uuid:pk>/", UpdateTask.as_view(), name="update_task"),
]