from django.db import models

class Course(models.Model):
    '''
    Modèle pour représenter une matière ou un cours.
    '''
    name = models.CharField(max_length=100, verbose_name="Nom du cours")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    code = models.CharField(max_length=20, unique=True, verbose_name="Code du cours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"
