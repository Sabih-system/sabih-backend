# views.py

from rest_framework import generics, permissions
from ..models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import BasePermission
from Team.models import Employee
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
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

    def get_object(self):
        user = self.request.user
        message = super().get_object()

        if ((hasattr(user, 'client') and (message.sender_client == user.client or message.receiver_client == user.client)) or
            (hasattr(user, 'employee') and (message.sender_employee == user.employee or message.receiver_employee == user.employee))):
            return message
        else:
            raise PermissionDenied("You do not have permission to view this message.")

class MessageUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]
    
    def perform_update(self , serializer):
        user = self.request.user
        print('serializer instance', serializer.instance.sender_client, serializer.instance.sender_employee)
        if hasattr(user, 'client') and serializer.instance.sender_client == user.client:
            serializer.save()
        elif hasattr(user, 'employee') and serializer.instance.sender_employee == user.employee:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to update this message.")

class MessageDeleteView(generics.DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrSupervisor]
    
    def perform_destroy(self, instance):
        user = self.request.user
        
        if hasattr(user, 'client') and instance.sender_client == user.client:
            instance.delete()
        elif hasattr(user, 'employee') and instance.sender_employee == user.employee:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this message.")
        
    
        
        
