from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherAvailabilityViewSet

router = DefaultRouter()
router.register(r'', TeacherAvailabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
