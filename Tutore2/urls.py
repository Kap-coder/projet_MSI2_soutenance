"""
URL configuration for Tutore2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('admin/', admin.site.urls),
    path('auth/', include(('users.urls','accounts'), namespace='accounts')),
    path('dashboard/', include('dashboard.urls')),
    path('rooms/', include('rooms.urls')),
    path('courses/', include('courses.urls')),
    path('departments/', include('users.urls_departments')),
    path('manage/users/', include('users.urls_manage')),
    path('availability/', include('availability.urls')),
]
