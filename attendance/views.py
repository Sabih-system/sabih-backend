from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Employee, Attendance, LateAttendance, LeaveRequest
from .forms import EmployeeForm

# Employee Views
class EmployeeListView(ListView):
    model = Employee
    template_name = 'attendance/employee_list.html'
    context_object_name = 'employees'

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'attendance/employee_detail.html'

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'attendance/employee_form.html'
    success_url = reverse_lazy('attendance:employee-list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'attendance/employee_form.html'
    success_url = reverse_lazy('attendance:employee-list')

# Attendance Views
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'

class AttendanceDetailView(DetailView):
    model = Attendance
    template_name = 'attendance/attendance_detail.html'

class AttendanceCreateView(CreateView):
    model = Attendance
    template_name = 'attendance/attendance_form.html'
    fields = ['employee', 'date', 'check_in_time', 'check_out_time', 'status']
    success_url = reverse_lazy('attendance:attendance-list')

# LateAttendance Views
class LateAttendanceListView(ListView):
    model = LateAttendance
    template_name = 'attendance/late_attendance_list.html'
    context_object_name = 'late_attendances'

class LateAttendanceCreateView(CreateView):
    model = LateAttendance
    template_name = 'attendance/late_attendance_form.html'
    fields = ['employee', 'date', 'check_in_time', 'reason']
    success_url = reverse_lazy('attendance:late-attendance-list')

# LeaveRequest Views
class LeaveRequestListView(ListView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_list.html'
    context_object_name = 'leave_requests'

class LeaveRequestDetailView(DetailView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_detail.html'

class LeaveRequestCreateView(CreateView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_form.html'
    fields = ['employee', 'start_date', 'end_date', 'leave_type', 'reason']
    success_url = reverse_lazy('attendance:leave-request-list')

class LeaveRequestUpdateView(UpdateView):
    model = LeaveRequest
    template_name = 'attendance/leave_request_form.html'
    fields = ['status']
    success_url = reverse_lazy('attendance:leave-request-list')