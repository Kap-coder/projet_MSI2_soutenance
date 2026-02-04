from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # Filiere URLs
    path('filieres/', views.FiliereListView.as_view(), name='filiere_list'),
    path('filieres/add/', views.FiliereCreateView.as_view(), name='filiere_add'),
    path('filieres/<int:pk>/edit/', views.FiliereUpdateView.as_view(), name='filiere_edit'),
    path('filieres/<int:pk>/delete/', views.FiliereDeleteView.as_view(), name='filiere_delete'),

    # Level URLs
    path('levels/', views.LevelListView.as_view(), name='level_list'),
    path('levels/add/', views.LevelCreateView.as_view(), name='level_add'),
    path('levels/<int:pk>/edit/', views.LevelUpdateView.as_view(), name='level_edit'),
    path('levels/<int:pk>/delete/', views.LevelDeleteView.as_view(), name='level_delete'),
]
