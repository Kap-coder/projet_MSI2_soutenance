from django.urls import path
from . import views
from .views_grid import AvailabilityGridView


app_name = 'availability'

urlpatterns = [
    path('', views.TeacherAvailabilityListView.as_view(), name='list'),
    path('grid/', AvailabilityGridView.as_view(), name='grid'),
    path('add/', views.TeacherAvailabilityCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.TeacherAvailabilityUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TeacherAvailabilityDeleteView.as_view(), name='delete'),
]
