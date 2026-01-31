from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''
    Modèle utilisateur personnalisé qui étend l'utilisateur de base de Django.
    Ajoute un champ `role` pour différencier les administrateurs, les enseignants et les étudiants.
    '''
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('TEACHER', 'Enseignant'),
        ('STUDENT', 'Étudiant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Rôle")

class Course(models.Model):
    '''
    Modèle pour représenter une matière ou un cours.
    '''
    name = models.CharField(max_length=100, verbose_name="Nom du cours")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name

class Room(models.Model):
    '''
    Modèle pour représenter une salle de classe.
    '''
    name = models.CharField(max_length=50, verbose_name="Nom de la salle")
    capacity = models.PositiveIntegerField(verbose_name="Capacité")

    def __str__(self):
        return self.name

class Timetable(models.Model):
    '''
    Modèle pour l'emploi du temps global.
    Il a un statut pour savoir s'il est en brouillon ou publié.
    '''
    STATUS_CHOICES = (
        ('DRAFT', 'Brouillon'),
        ('PUBLISHED', 'Publié'),
    )
    name = models.CharField(max_length=150, verbose_name="Nom de l'emploi du temps")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TimeSlot(models.Model):
    '''
    Modèle pour un créneau horaire spécifique dans un emploi du temps.
    Lie un cours, un enseignant, une salle à un moment précis.
    '''
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='time_slots', verbose_name="Emploi du temps")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Cours")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle")
    start_time = models.DateTimeField(verbose_name="Heure de début")
    end_time = models.DateTimeField(verbose_name="Heure de fin")

    def __str__(self):
        return f"{self.course.name} avec {self.teacher.get_full_name()} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class TeacherAvailability(models.Model):
    '''
    Modèle pour que les enseignants puissent indiquer leurs disponibilités.
    '''
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'TEACHER'}, verbose_name="Enseignant")
    start_time = models.DateTimeField(verbose_name="Début de disponibilité")
    end_time = models.DateTimeField(verbose_name="Fin de disponibilité")

    def __str__(self):
        return f"Disponibilité de {self.teacher.get_full_name()} du {self.start_time} au {self.end_time}"