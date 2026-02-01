from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'user', 'year', 'department', 'enrollment_status']
    list_filter = ['enrollment_status', 'year', 'department', 'enrollment_date']
    search_fields = ['matricule', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['enrollment_date', 'validated_date']
    
    fieldsets = (
        ('Informations d\'étudiant', {
            'fields': ('user', 'matricule', 'year', 'department')
        }),
        ('Statut d\'inscription', {
            'fields': ('enrollment_status', 'enrollment_date', 'validated_date', 'validated_by', 'rejection_reason')
        }),
    )
