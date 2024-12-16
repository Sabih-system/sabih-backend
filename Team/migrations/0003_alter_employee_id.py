# Generated by Django 5.1.3 on 2024-12-16 00:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0002_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]