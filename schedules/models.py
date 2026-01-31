from django.db import models
from django.core.exceptions import ValidationError
from timetables.models import Timetable
from courses.models import Course
from rooms.models import Room
from users.models import User

class TimeSlot(models.Model):
    '''
    Modèle pour un créneau horaire spécifique dans un emploi du temps.
    Lie un cours, un enseignant, une salle à un moment précis.
    '''
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='time_slots', verbose_name="Emploi du temps")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Cours", related_name='time_slots')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant", related_name='taught_slots')
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
