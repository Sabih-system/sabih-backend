from django.db import models
from django.utils import timezone
from django.db import models
from Account.models import User
import uuid


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique= True,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="employee")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100) 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    dob = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_hired = models.DateTimeField(auto_now_add=True)
    ROLE_CHOICES = [
        ('employee', 'EMPLOYEE'),
        ('manager', 'MANAGER'),
        ('supervisor', 'SUPERVISOR'),
    ]
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='employee')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)

    photo = models.ImageField(
        upload_to='employee', null=True, blank=True , default="employee/default.webp")

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique= True,editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True)
    assigner = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, related_name='assigner')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_completed:
            self.completed_date = timezone.now()
        super().save(*args, **kwargs)