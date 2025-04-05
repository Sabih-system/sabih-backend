from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    email = models.EmailField(unique=True)
    qr_code_token = models.UUIDField(default=uuid.uuid4, unique=True)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        # Ensure password is hashed if it's being set (typically done by Django automatically)
        if self.pk is None and self.password:  # Check if the password is being set for a new user
            self.password = make_password(self.password)  # Hash the password

        qr_data = str(self.qr_code_token)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create an image of the QR code
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Save the QR code image to the `qr_code_image` field
        self.qr_code_image.save(f"{self.username}_qr.png", ContentFile(buffer.read()), save=False)
        buffer.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}"
