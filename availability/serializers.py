from rest_framework import serializers
from .models import TeacherAvailability

class TeacherAvailabilitySerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = TeacherAvailability
        fields = ['id', 'teacher', 'teacher_name', 'day_of_week', 'day_display', 'start_time', 'end_time', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
