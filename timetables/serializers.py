from rest_framework import serializers
from .models import Timetable

class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timetable
        fields = ['id', 'name', 'description', 'academic_year', 'semester', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TimetableDetailSerializer(serializers.ModelSerializer):
    time_slots = serializers.SerializerMethodField()
    
    class Meta:
        model = Timetable
        fields = ['id', 'name', 'description', 'academic_year', 'semester', 'status', 'time_slots', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_time_slots(self, obj):
        from schedules.serializers import TimeSlotSerializer
        return TimeSlotSerializer(obj.time_slots.all(), many=True).data
