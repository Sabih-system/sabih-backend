# Generated by Django 5.1.3 on 2024-12-06 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0003_remove_user_qr_code_image_user_barcode_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='barcode_image',
        ),
        migrations.AddField(
            model_name='user',
            name='qr_code_image',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
