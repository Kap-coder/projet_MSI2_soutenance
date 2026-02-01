from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from enrollments.models import StudentProfile
from timetables.models import Timetable, TimeSlot

User = get_user_model()


@login_required(login_url='users:login')
def home(request):
    '''
    Vue d'accueil du dashboard avec redirection selon le rôle.
    '''
    user = request.user
    
    context = {
        'user': user,
    }
    
    if user.role == 'STUDENT':
        # Dashboard étudiant
        try:
            student = user.student_profile
            context['student'] = student
            context['enrollment_status'] = student.get_enrollment_status_display()
            
            if student.enrollment_status == 'APPROVED':
                # Afficher l'emploi du temps
                timetable = Timetable.objects.filter(
                    academic_year='2025-2026'  # À adapter
                ).first()
                if timetable:
                    context['timetable'] = timetable
                    context['time_slots'] = timetable.time_slots.all()[:10]
        except StudentProfile.DoesNotExist:
            pass
        
        return render(request, 'dashboard/student_dashboard.html', context)
    
    elif user.role == 'TEACHER':
        # Dashboard enseignant
        context['taught_slots'] = TimeSlot.objects.filter(teacher=user)[:10]
        return render(request, 'dashboard/teacher_dashboard.html', context)
    
    elif user.role == 'DEPARTMENT_HEAD':
        # Dashboard chef de département
        if hasattr(user, 'headed_department'):
            context['department'] = user.headed_department
            context['students'] = StudentProfile.objects.filter(
                department=user.headed_department,
                enrollment_status='PENDING'
            )[:10]
            context['pending_count'] = context['students'].count()
        
        return render(request, 'dashboard/head_dashboard.html', context)
    
    elif user.role == 'HR':
        # Dashboard RH
        context['total_users'] = User.objects.count()
        context['pending_students'] = StudentProfile.objects.filter(enrollment_status='PENDING').count()
        return render(request, 'dashboard/hr_dashboard.html', context)
    
    elif user.role == 'RESOURCE_MANAGER':
        # Dashboard gestionnaire de ressources
        from rooms.models import Room
        context['total_rooms'] = Room.objects.count()
        context['available_rooms'] = Room.objects.filter(is_available=True).count()
        return render(request, 'dashboard/rm_dashboard.html', context)
    
    elif user.role == 'ADMIN':
        # Dashboard administrateur
        context['total_users'] = User.objects.count()
        context['total_students'] = User.objects.filter(role='STUDENT').count()
        context['pending_enrollments'] = StudentProfile.objects.filter(enrollment_status='PENDING').count()
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    return render(request, 'dashboard/home.html', context)
