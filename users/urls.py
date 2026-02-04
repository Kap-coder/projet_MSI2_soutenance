from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/student/', views.login_student_view, name='login_student'),
    path('login/admin/', views.login_admin_view, name='login_admin'),
    path('selection/', views.selection_view, name='selection'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
