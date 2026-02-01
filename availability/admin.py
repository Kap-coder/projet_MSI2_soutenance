from django.contrib import admin
from .models import TeacherAvailability

@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('teacher__username', 'teacher__last_name', 'teacher__first_name')
