from django.db import models

class Course(models.Model):
    '''
    Modèle pour représenter une matière ou un cours.
    '''
    name = models.CharField(max_length=100, verbose_name="Nom du cours")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code du cours")
    
    # New fields
    department = models.ForeignKey('users.Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Filière/Département", related_name='courses')
    teachers = models.ManyToManyField('users.User', limit_choices_to={'role': 'TEACHER'}, blank=True, verbose_name="Enseignants", related_name='courses_taught')
    
    LEVEL_CHOICES = (
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
        ('D', 'Doctorat'),
    )
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES, blank=True, null=True, verbose_name="Niveau")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"
