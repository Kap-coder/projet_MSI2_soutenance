from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='list'),
    path('teacher/', views.TeacherCourseListView.as_view(), name='teacher_list'),
    path('teacher/<int:pk>/', views.TeacherCourseDetailView.as_view(), name='teacher_detail'),
    path('add/', views.CourseCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='delete'),
]
