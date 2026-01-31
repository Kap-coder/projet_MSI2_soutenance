from django.db import models

class Room(models.Model):
    '''
    Modèle pour représenter une salle de classe.
    '''
    ROOM_TYPE = (
        ('CLASSROOM', 'Salle de classe'),
        ('LAB', 'Laboratoire'),
        ('AMPHITHEATER', 'Amphithéâtre'),
    )
    
    name = models.CharField(max_length=50, verbose_name="Nom de la salle", unique=True)
    capacity = models.PositiveIntegerField(verbose_name="Capacité")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE, default='CLASSROOM', verbose_name="Type de salle")
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Capacité: {self.capacity})"
