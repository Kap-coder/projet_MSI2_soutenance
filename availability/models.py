from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class TeacherAvailability(models.Model):
    '''
    Disponibilités semaine/time pour enseignants.
    '''
    DAYS_OF_WEEK = (
        (0, 'Lundi'),
        (1, 'Mardi'),
        (2, 'Mercredi'),
        (3, 'Jeudi'),
        (4, 'Vendredi'),
        (5, 'Samedi'),
        (6, 'Dimanche'),
    )

    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant", related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, verbose_name="Jour de la semaine")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    start_date = models.DateField(null=True, blank=True, verbose_name="Date de début (Période)")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin (Période)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Disponibilité enseignant"
        verbose_name_plural = "Disponibilités enseignants"
        ordering = ['day_of_week', 'start_time']
        unique_together = ('teacher', 'day_of_week', 'start_time', 'end_time')

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Disponibilité de {self.teacher.get_full_name()} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"
