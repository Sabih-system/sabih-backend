from django.db import models
from Account.models import User
import uuid

class Client ( models.Model ):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.company
    
class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proposals", null=False)
    project_type = models.CharField(max_length=200)
    budget = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    is_approved = models.BooleanField(default=False)  
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.company} - {self.project_type}"

    