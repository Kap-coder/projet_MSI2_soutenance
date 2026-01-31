from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'capacity', 'location', 'is_available']
    list_filter = ['room_type', 'is_available', 'created_at']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'room_type', 'capacity', 'location')
        }),
        ('Statut', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
