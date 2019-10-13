from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
#Se crean las clases de acuerdo con el diagrama de clases
class Cliente(models.Model):
    dni = models.PositiveIntegerField('DNI',primary_key=True, validators=[MinValueValidator(1000000),MaxValueValidator(9999999)])
    apellido = models.CharField('Apellidos',max_length=100, blank=False, null=False)
    nombre = models.CharField('Nombres',max_length=100, blank=False, null=False)
    telefono = models.CharField('Telefonos',max_length=50)
    correo = models.EmailField('Correos')
    domicilio = models.CharField('Domicilios',blank = True, null = True, max_length=500)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido']

    def __str__(self):
        return str(self.dni) + ' | ' + self.apellido + ' ' + self.nombre
