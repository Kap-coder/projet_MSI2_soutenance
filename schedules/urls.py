from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('config/', views.GlobalTimeSlotListView.as_view(), name='list'),
    path('config/add/', views.GlobalTimeSlotCreateView.as_view(), name='add'),
    path('config/generate/', views.ScheduleGeneratorView.as_view(), name='generate'),
    path('config/<int:pk>/edit/', views.GlobalTimeSlotUpdateView.as_view(), name='edit'),
    path('config/<int:pk>/delete/', views.GlobalTimeSlotDeleteView.as_view(), name='delete'),
]
