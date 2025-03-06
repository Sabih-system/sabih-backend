from django.contrib import admin
from .models import Employee, Attendance

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'position', 'department', 'is_active')
    search_fields = ('name', 'email', 'position', 'department')
    list_filter = ('is_active',)  # Removed 'role'

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in_time')
    list_filter = ('status', 'date')
    search_fields = ('employee__name', 'employee__email')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
