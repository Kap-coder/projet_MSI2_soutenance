from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'get_level', 'filiere', 'total_hours', 'created_at']
    list_filter = ['filiere__department', 'filiere', 'level', 'created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'name', 'description')
        }),
        ('Organisation Académique', {
            'fields': ('filiere', 'level', 'total_hours', 'teachers')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_level(self, obj):
        return f"{obj.level.name}" if obj.level else "-"
    get_level.short_description = "Niveau"
