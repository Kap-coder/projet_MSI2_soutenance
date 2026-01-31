from django.contrib import admin
from .models import Timetable

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_year', 'semester', 'status', 'created_at']
    list_filter = ['status', 'semester', 'academic_year', 'created_at']
    search_fields = ['name', 'academic_year']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'academic_year', 'semester')
        }),
        ('Statut', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
