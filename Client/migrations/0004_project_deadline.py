# Generated by Django 5.1.3 on 2025-06-23 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Client', '0003_client_date_created_project_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
    ]
