# Generated by Django 5.1.3 on 2024-12-21 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Team', '0004_alter_employee_id_alter_employee_user_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigner', to='Team.employee'),
        ),
    ]
