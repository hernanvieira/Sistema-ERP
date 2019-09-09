from django.db import models

# Create your models here.
#Se crean las clases de acuerdo con el diagrama de clases
class Cliente(models.Model):
    dni = models.CharField(max_length=10, blank=False, null=False, primary_key=True)
    apellido = models.CharField(max_length=100, blank=False, null=False)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.IntegerField(blank=False, null=False)
    correo = models.CharField(max_length=200, blank=False, null=False)
    domicilio = models.TextField(blank = True, null = True)
    activo = models.BooleanField()
