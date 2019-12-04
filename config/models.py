from django.db import models

class Configuracion (models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    empresa = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255)
    logo = models.BinaryField(blank = True, null=True )
