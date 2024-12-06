# Generated by Django 5.1.3 on 2024-12-06 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('dob', models.DateField()),
                ('position', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('date_hired', models.DateTimeField(auto_now_add=True)),
                ('role', models.CharField(choices=[('employee', 'EMPLOYEE'), ('manager', 'MANAGER'), ('supervisor', 'SUPERVISOR')], default='employee', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='employee')),
            ],
        ),
    ]