from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    '''
    Modèle utilisateur personnalisé qui étend l'utilisateur de base de Django.
    Ajoute un champ `role` pour différencier les différents rôles.
    '''
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('TEACHER', 'Enseignant'),
        ('STUDENT', 'Étudiant'),
        ('DEPARTMENT_HEAD', 'Chef de département'),
        ('HR', 'Ressources Humaines'),
        ('RESOURCE_MANAGER', 'Gestionnaire de ressources'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Rôle")

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"


class Department(models.Model):
    """
    Département de l'établissement.
    Déplacé ici pour réduire le nombre d'apps.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du département")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code du département")
    description = models.TextField(blank=True, verbose_name="Description")
    head = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                limit_choices_to={'role': 'DEPARTMENT_HEAD'},
                                verbose_name="Chef de département", related_name='headed_department')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class LoginLog(models.Model):
    '''
    Log de connexions pour audit.
    '''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_logs', verbose_name="Utilisateur")
    ip_address = models.GenericIPAddressField(verbose_name="Adresse IP")
    user_agent = models.TextField(verbose_name="User Agent")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Heure de connexion")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Heure de déconnexion")
    is_successful = models.BooleanField(default=True, verbose_name="Connexion réussie")
    failure_reason = models.CharField(max_length=255, blank=True, verbose_name="Raison de l'échec")

    class Meta:
        verbose_name = "Log de connexion"
        verbose_name_plural = "Logs de connexion"
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class RememberMeToken(models.Model):
    '''
    Token pour fonctionnalité "Se souvenir de moi".
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='remember_token', verbose_name="Utilisateur")
    token = models.CharField(max_length=255, unique=True, verbose_name="Token")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name="Expiration")

    class Meta:
        verbose_name = "Token de mémorisation"
        verbose_name_plural = "Tokens de mémorisation"

    def __str__(self):
        return f"Token pour {self.user.username}"



