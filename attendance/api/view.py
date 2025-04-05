from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Employee, Attendance, LateAttendance, LeaveRequest
from .serializers import (
    EmployeeSerializer, AttendanceSerializer,
    LateAttendanceSerializer, LeaveRequestSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def attendance_history(self, request, pk=None):
        employee = self.get_object()
        attendances = Attendance.objects.filter(employee=employee)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def scan_barcode(self, request):
        barcode = request.data.get('barcode_id')
        try:
            employee = Employee.objects.get(barcode_id=barcode)
            today = timezone.localtime().date()
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today
            )
            attendance.process_barcode_scan()
            serializer = self.get_serializer(attendance)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Invalid barcode'},
                status=status.HTTP_400_BAD_REQUEST
            )

class LateAttendanceViewSet(viewsets.ModelViewSet):
    queryset = LateAttendance.objects.all()
    serializer_class = LateAttendanceSerializer
    permission_classes = [IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        leave_request = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(LeaveRequest.STATUS_CHOICES):
            leave_request.status = new_status
            leave_request.save()
            serializer = self.get_serializer(leave_request)
            return Response(serializer.data)
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )