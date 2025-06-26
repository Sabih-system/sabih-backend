from rest_framework import serializers
from ..models import Employee, Task
from Account.api.serializers import UserSerializer
from Account.models import User

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True,
        required=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'user_id', 'user', 'name', 'type', 'email', 'phone',
            'address', 'dob', 'position', 'department', 'date_hired',
            'role', 'is_active', 'start_date', 'end_date', 'photo'
        ]


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'employee', 'assigner','project', 'title', 'description',
                  'start_date', 'deadline', 'is_completed', 'completed_date']
