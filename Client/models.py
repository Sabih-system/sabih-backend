from django.db import models

# Create your models here.
from django.db import models


class UsersideRequest(models.Model):
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email_address = models.EmailField()
    attach_proposal = models.FileField(upload_to='proposals/', null=True, blank=True)
    work_description = models.TextField(help_text="Describe the work you want us to do.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company_name} - {self.name}"
