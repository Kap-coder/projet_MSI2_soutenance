from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Room
from .serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'capacity', 'created_at']
    filterset_fields = ['room_type', 'is_available']
