from django.db import models
from django.core.exceptions import ValidationError
from courses.models import Course
from rooms.models import Room
from django.conf import settings

class Timetable(models.Model):
    '''
    Modèle pour l'emploi du temps global.
    Il a un statut pour savoir s'il est en brouillon ou publié.
    '''
    STATUS_CHOICES = (
        ('DRAFT', 'Brouillon'),
        ('PUBLISHED', 'Publié'),
        ('ARCHIVED', 'Archivé'),
    )
    
    name = models.CharField(max_length=150, verbose_name="Nom de l'emploi du temps")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT', verbose_name="Statut")
    academic_year = models.CharField(max_length=20, verbose_name="Année académique")
    semester = models.CharField(max_length=20, choices=[('S1', 'Semestre 1'), ('S2', 'Semestre 2')], verbose_name="Semestre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['-created_at']
        unique_together = ('academic_year', 'semester')

    def __str__(self):
        return f"{self.name} ({self.academic_year} - {self.get_semester_display()})"


class TimeSlot(models.Model):
    '''
    Créneau horaire lié à un `Timetable`.
    '''
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='time_slots', verbose_name="Emploi du temps")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Cours", related_name='time_slots')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant", related_name='taught_slots')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle", related_name='time_slots')
    start_time = models.DateTimeField(verbose_name="Heure de début")
    end_time = models.DateTimeField(verbose_name="Heure de fin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Créneau horaire"
        verbose_name_plural = "Créneaux horaires"
        ordering = ['start_time']
        unique_together = ('timetable', 'room', 'start_time', 'end_time')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} avec {self.teacher.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
