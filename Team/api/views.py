from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Team.api.serializers import EmployeeSerializer, TaskSerializer
from Team.models import Employee, Task
from rest_framework.views import APIView


class EmployeeCreationView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class TaskCreationView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if (user.employee.role == 'manager'):
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['assigner'] = user.employee

                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        return Response({'error': 'Only Admin can create task'}, status=400)


class GetEmployeeTasks(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        employee = get_object_or_404(Employee, user=user)
        return Task.objects.filter(employee=employee)


class UpdateTask(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(employee=self.request.user.employee)
