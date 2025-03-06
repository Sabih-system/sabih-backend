from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
from django.conf import settings
class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employee")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_hired = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(default=timezone.now)
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('LATE', 'Late'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('employee', 'date')  # Prevent duplicate attendance for the same day

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

class LateAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,  related_name="attendance_employee")
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)  # Optional reason

    def __str__(self):
        return f"{self.employee.name} - {self.date} - Late"
