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

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
