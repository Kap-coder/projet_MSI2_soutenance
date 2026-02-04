from django.db import models

class Course(models.Model):
    '''
    Modèle pour représenter une matière ou un cours.
    '''
    name = models.CharField(max_length=100, verbose_name="Nom du cours")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code du cours")
    
    # New fields
    # Updated fields for new hierarchy
    level = models.ForeignKey('users.Level', on_delete=models.CASCADE, verbose_name="Niveau", related_name='courses', null=True, blank=True)
    teachers = models.ManyToManyField('users.User', limit_choices_to={'role': 'TEACHER'}, blank=True, verbose_name="Enseignants", related_name='courses_taught')
    
    # LEVEL_CHOICES deleted as we now use a dedicated model

    
    total_hours = models.PositiveIntegerField(default=0, verbose_name="Volume Horaire Total (Semestre)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"
