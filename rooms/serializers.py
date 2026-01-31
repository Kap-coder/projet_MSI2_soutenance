from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'room_type', 'capacity', 'location', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
