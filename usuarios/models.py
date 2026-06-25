from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Perfil(models.Model):

    ROLES = [
        ('Recepcionista', 'Recepcionista'),
        ('Veterinario', 'Veterinario'),
        ('Administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    
    def __str__(self):
        return f"{self.user.first_name} - {self.rol}"

