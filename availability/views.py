from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import TeacherAvailability
from .serializers import TeacherAvailabilitySerializer

class TeacherAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = TeacherAvailability.objects.all()
    serializer_class = TeacherAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['teacher__first_name', 'teacher__last_name']
    ordering_fields = ['day_of_week', 'start_time']
    filterset_fields = ['teacher', 'day_of_week', 'is_active']
