from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('student/', views.student_dashboard, name='student'),
    path('department-head/', views.head_dashboard, name='head'),
    path('hr/', views.hr_dashboard, name='hr'),
    path('resource-manager/', views.rm_dashboard, name='rm'),
]
