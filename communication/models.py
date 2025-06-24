from django.db import models
from django.conf import settings
from Client.models import Client
from Team.models import Employee


# models.py

class Message(models.Model):
    MESSAGE_TYPES = [
        ('text', 'Text'),
        ('file', 'File with text'),
    ]

    sender_client = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages_client'
    )
    sender_employee = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='sent_messages_employee'
    )
    receiver_client = models.ForeignKey(
        Client, null=True, blank=True, on_delete=models.SET_NULL, related_name='received_messages_client'
    )
    receiver_employee = models.ForeignKey(
        Employee, null=True, blank=True, on_delete=models.SET_NULL, related_name='received_messages_employee'
    )

    content = models.TextField(blank=True)
    file = models.FileField(upload_to='messages/files/', null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message at {self.timestamp}"
