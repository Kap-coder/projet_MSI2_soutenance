from django.contrib import admin
from .models import TimeSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['course', 'teacher', 'room', 'start_time', 'end_time']
    list_filter = ['timetable', 'course', 'teacher', 'room', 'start_time']
    search_fields = ['course__name', 'teacher__first_name', 'teacher__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('timetable', 'course', 'teacher', 'room')
        }),
        ('Horaires', {
            'fields': ('start_time', 'end_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si c'est une modification
            return self.readonly_fields + ['timetable']
        return self.readonly_fields
