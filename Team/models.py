from django.db import models


from django.db import models
from Account.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        upload_to='employee', null=True, blank=True)

    def __str__(self):
        return self.name
