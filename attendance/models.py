from django.db import models
from django.utils import timezone
import uuid
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
    barcode_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('LATE', 'Late'),
        ('ABSENT', 'Absent'),
        ('ON_LEAVE', 'On Leave'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ABSENT')
    is_checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"

    def process_barcode_scan(self):
        current_time = timezone.localtime().time()
        
        if not self.is_checked_in:
            # This is a check-in
            self.check_in_time = current_time
            self.is_checked_in = True
            self.set_status()
        else:
            # This is a check-out
            self.check_out_time = current_time
            self.is_checked_in = False
        self.save()

    def set_status(self):
        if not self.check_in_time:
            # If no check-in by end of day, mark as absent
            if timezone.localtime().time() > timezone.datetime.strptime('23:59', '%H:%M').time():
                self.status = 'ABSENT'
            return

        # Check if employee is on approved leave
        leave_request = LeaveRequest.objects.filter(
            employee=self.employee,
            start_date__lte=self.date,
            end_date__gte=self.date,
            status='APPROVED'
        ).first()

        if leave_request:
            self.status = 'ON_LEAVE'
            return

        # Set the cutoff time for "late" (9:00 AM)
        cutoff_time = timezone.datetime.strptime('09:00', '%H:%M').time()
        
        if self.check_in_time > cutoff_time:
            self.status = 'LATE'
        else:
            self.status = 'PRESENT'

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Check for existing leave request
            leave_request = LeaveRequest.objects.filter(
                employee=self.employee,
                start_date__lte=self.date,
                end_date__gte=self.date,
                status='APPROVED'
            ).first()
            if leave_request:
                self.status = 'ON_LEAVE'

        self.set_status()
        super().save(*args, **kwargs)

class LateAttendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_employee")
    date = models.DateField(default=timezone.now)
    check_in_time = models.TimeField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.employee.name} - {self.date} - Late"

class LeaveRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    LEAVE_TYPES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation'),
        ('PERSONAL', 'Personal'),
        ('OTHER', 'Other'),
    ]
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    reason = models.TextField()
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.name} - {self.leave_type} ({self.start_date} to {self.end_date})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'APPROVED':
            # Update any existing attendance records within the leave period
            Attendance.objects.filter(
                employee=self.employee,
                date__range=[self.start_date, self.end_date]
            ).update(status='ON_LEAVE')
