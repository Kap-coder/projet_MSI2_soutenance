from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'get_level', 'total_hours', 'created_at']
    list_filter = ['level__filiere__department', 'level__filiere', 'level', 'created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'name', 'description')
        }),
        ('Organisation Académique', {
            'fields': ('level', 'total_hours', 'teachers')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_level(self, obj):
        return f"{obj.level.name} ({obj.level.filiere.name})" if obj.level else "-"
    get_level.short_description = "Niveau"
