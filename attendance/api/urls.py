from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'api/employees', api.EmployeeViewSet)
router.register(r'api/attendance', api.AttendanceViewSet)
router.register(r'api/late-attendance', api.LateAttendanceViewSet)
router.register(r'api/leave-requests', api.LeaveRequestViewSet)

app_name = 'attendance'

urlpatterns = [
    # Your existing URL patterns...
    
    # API URLs
    path('', include(router.urls)),
]