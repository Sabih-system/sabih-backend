# views.py

from rest_framework import generics, permissions
from ..models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import BasePermission
from Team.models import Employee
from django.db.models import Q

class IsClientOrSupervisor(BasePermission):
    def has_permission(self, request, view):
        try:
            employee = request.user.employee
            return employee.role.lower() == 'supervisor' or hasattr(request.user, 'client')
        except Employee.DoesNotExist:
            return False
        
  


class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]

    def get_queryset(self):
        user = self.request.user
        with_client_id = self.request.query_params.get("with_client")
        with_employee_id = self.request.query_params.get("with_employee")
        print(f"with_client_id: {with_client_id}, with_employee_id: {with_employee_id}")
        print("User:", user)
        print("Has client:", hasattr(user, 'client'))
        print("Has employee:", hasattr(user, 'employee'))

        if hasattr(user, 'client') and with_employee_id:
            return Message.objects.filter(
                Q(sender_client=user.client, receiver_employee__id=with_employee_id) |
                Q(sender_employee__id=with_employee_id, receiver_client=user.client)
            ).order_by('timestamp')

        elif hasattr(user, 'employee')  and with_client_id:
            return Message.objects.filter(
                Q(sender_employee=user.employee, receiver_client__id=with_client_id) |
                Q(sender_client__id=with_client_id, receiver_employee=user.employee)
            ).order_by('timestamp')
        print("No client or employee found for user.")
        return Message.objects.none()



    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, 'client'):
            serializer.save(sender_client=user.client)
        elif hasattr(user, 'employee') and user.employee.role == 'supervisor':
            serializer.save(sender_employee=user.employee)
            
            
class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]


class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]

class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]
