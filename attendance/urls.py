from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Employee URLs
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employee/<uuid:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<uuid:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),

    # Attendance URLs
    path('attendance/', views.AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance-create'),

    # Late Attendance URLs
    path('late-attendance/', views.LateAttendanceListView.as_view(), name='late-attendance-list'),
    path('late-attendance/create/', views.LateAttendanceCreateView.as_view(), name='late-attendance-create'),

    # Leave Request URLs
    path('leave-requests/', views.LeaveRequestListView.as_view(), name='leave-request-list'),
    path('leave-request/<uuid:pk>/', views.LeaveRequestDetailView.as_view(), name='leave-request-detail'),
    path('leave-request/create/', views.LeaveRequestCreateView.as_view(), name='leave-request-create'),
    path('leave-request/<uuid:pk>/update/', views.LeaveRequestUpdateView.as_view(), name='leave-request-update'),
]