from django.db import models
from users.models import User, Department

class StudentProfile(models.Model):
    '''
    Profil d'étudiant avec informations supplémentaires.
    '''
    YEAR_CHOICES = (
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    )
    
    ENROLLMENT_STATUS = (
        ('PENDING', 'En attente de validation'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', verbose_name="Utilisateur")
    matricule = models.CharField(max_length=20, unique=True, verbose_name="Matricule")
    year = models.CharField(max_length=3, choices=YEAR_CHOICES, verbose_name="Niveau d'étude")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Département", related_name='students')
    enrollment_status = models.CharField(max_length=10, choices=ENROLLMENT_STATUS, default='PENDING', verbose_name="Statut d'inscription")
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    validated_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'DEPARTMENT_HEAD'}, verbose_name="Validé par", related_name='validated_enrollments')
    rejection_reason = models.TextField(blank=True, verbose_name="Raison du rejet")

    class Meta:
        verbose_name = "Profil étudiant"
        verbose_name_plural = "Profils étudiants"
        ordering = ['-enrollment_date']

    def __str__(self):
        return f"{self.matricule} - {self.user.get_full_name()}"
