from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
