from django.contrib import admin
from .models import TeacherAvailability

@admin.register(TeacherAvailability)
class TeacherAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'day_of_week', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active', 'teacher']
    search_fields = ['teacher__first_name', 'teacher__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('teacher', 'day_of_week')
        }),
        ('Horaires', {
            'fields': ('start_time', 'end_time')
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
