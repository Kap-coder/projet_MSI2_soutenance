from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Schedule(models.Model):
    """
    Créneau horaire planifié.
    Ce modèle est une ébauche basée sur la documentation.
    """
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, verbose_name="Cours", related_name='schedules')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant")
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE, verbose_name="Salle")
    timetable = models.ForeignKey('timetables.Timetable', on_delete=models.CASCADE, verbose_name="Emploi du temps", related_name='schedules')
    
    day_of_week = models.IntegerField(choices=[
        (0, 'Lundi'), (1, 'Mardi'), (2, 'Mercredi'), 
        (3, 'Jeudi'), (4, 'Vendredi'), (5, 'Samedi'), (6, 'Dimanche')
    ], verbose_name="Jour")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Créneau Horaire"
        verbose_name_plural = "Créneaux Horaires"
        ordering = ['day_of_week', 'start_time']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

    def __str__(self):
        return f"{self.course} - {self.get_day_of_week_display()} {self.start_time}"
