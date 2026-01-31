from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TimeSlot
from .serializers import TimeSlotSerializer

class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['course__name', 'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['start_time', 'created_at']
    filterset_fields = ['timetable', 'course', 'teacher', 'room']
