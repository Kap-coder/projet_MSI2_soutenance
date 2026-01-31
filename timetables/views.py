from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Timetable
from .serializers import TimetableSerializer, TimetableDetailSerializer

class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.all()
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'academic_year']
    ordering_fields = ['created_at', 'academic_year']
    filterset_fields = ['status', 'semester', 'academic_year']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TimetableDetailSerializer
        return TimetableSerializer
