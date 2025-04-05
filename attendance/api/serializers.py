from rest_framework import serializers
from .models import Employee, Attendance, LateAttendance, LeaveRequest

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'name', 'email', 'phone', 'position', 
                 'department', 'date_hired', 'is_active', 'barcode_id']
        read_only_fields = ['id', 'date_hired']

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'date', 'check_in_time', 
                 'check_out_time', 'status', 'is_checked_in']
        read_only_fields = ['status', 'is_checked_in']

class LateAttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = LateAttendance
        fields = ['id', 'employee', 'employee_name', 'date', 'check_in_time', 'reason']

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee', 'employee_name', 'start_date', 'end_date', 
                 'leave_type', 'reason', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']