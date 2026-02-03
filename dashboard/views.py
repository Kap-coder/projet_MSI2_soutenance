from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from enrollments.models import StudentProfile
from timetables.models import Timetable, TimeSlot
from rooms.models import Room

User = get_user_model()

@login_required(login_url='users:login')
def home(request):
    '''
    Vue d'accueil qui redirige vers le bon dashboard.
    '''
    user = request.user
    if user.role == 'ADMIN':
        return redirect('dashboard:admin')
    elif user.role == 'TEACHER':
        return redirect('dashboard:teacher')
    elif user.role == 'STUDENT':
        return redirect('dashboard:student')
    elif user.role == 'DEPARTMENT_HEAD':
        return redirect('dashboard:head')
    elif user.role == 'HR':
        return redirect('dashboard:hr')
    elif user.role == 'RESOURCE_MANAGER':
        return redirect('dashboard:rm')
    
    return render(request, 'dashboard/home.html', {'user': user})

@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard:home')
    
    context = {
        'total_users': User.objects.count(),
        'total_students': User.objects.filter(role='STUDENT').count(),
        'pending_enrollments': StudentProfile.objects.filter(enrollment_status='PENDING').count(),
        'user': request.user
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return redirect('dashboard:home')
    
    context = {
        'taught_slots': TimeSlot.objects.filter(teacher=request.user)[:10],
        'user': request.user
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)

@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return redirect('dashboard:home')
    
    context = {'user': request.user}
    try:
        student = request.user.student_profile
        context['student'] = student
        context['enrollment_status'] = student.get_enrollment_status_display()
        
        if student.enrollment_status == 'APPROVED':
            # Afficher l'emploi du temps (Logique temporaire)
            timetable = Timetable.objects.filter(
                academic_year='2025-2026'
            ).first()
            if timetable:
                context['timetable'] = timetable
                context['time_slots'] = timetable.time_slots.all()[:10]
    except StudentProfile.DoesNotExist:
        pass
    
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def head_dashboard(request):
    if request.user.role != 'DEPARTMENT_HEAD':
        return redirect('dashboard:home')
    
    context = {'user': request.user}
    if hasattr(request.user, 'headed_department'):
        context['department'] = request.user.headed_department
        context['students'] = StudentProfile.objects.filter(
            department=request.user.headed_department,
            enrollment_status='PENDING'
        )[:10]
        context['pending_count'] = context['students'].count()
    
    return render(request, 'dashboard/head_dashboard.html', context)

@login_required
def hr_dashboard(request):
    if request.user.role != 'HR':
        return redirect('dashboard:home')
    
    context = {
        'total_users': User.objects.count(),
        'pending_students': StudentProfile.objects.filter(enrollment_status='PENDING').count(),
        'user': request.user
    }
    return render(request, 'dashboard/hr_dashboard.html', context)

@login_required
def rm_dashboard(request):
    if request.user.role != 'RESOURCE_MANAGER':
        return redirect('dashboard:home')
    
    context = {
        'total_rooms': Room.objects.count(),
        'available_rooms': Room.objects.filter(is_available=True).count(),
        'user': request.user
    }
    return render(request, 'dashboard/rm_dashboard.html', context)
