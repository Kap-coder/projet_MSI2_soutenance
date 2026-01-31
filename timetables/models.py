from django.db import models

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
