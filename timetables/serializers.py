from rest_framework import serializers
from .models import Timetable, TimeSlot

class TimeSlotSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['id', 'timetable', 'course', 'course_name', 'teacher', 'teacher_name', 'room', 'room_name', 'start_time', 'end_time', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

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
        return TimeSlotSerializer(obj.time_slots.all(), many=True).data
