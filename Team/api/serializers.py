from rest_framework import serializers
from ..models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user' , 'name', 'type', 'email', 'phone', 'address', 'dob', 'position', 'department', 'date_hired', 'role', 'is_active', 'start_date', 'end_date', 'photo']