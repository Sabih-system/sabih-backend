from django.db import models
from Account.models import User


class Client ( models.Model ):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    company = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client")
    
    
    def __str__(self):
        return self.company
    
class Project(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    project_type = models.CharField(max_length=200)
    budget = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    client = models.ForeignKey(Client , on_delete=models.SET_NULL, null=True , related_name="projects")
    
    
    def __str__(self):
        return f"{self.company}-{self.project_type}"
    