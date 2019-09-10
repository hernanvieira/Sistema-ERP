from django.db import models

# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Estado (models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)

class Estado_pedido (models.Model):
    fecha = models.DateField()

class Estado_prenda (models.Model):
    fecha = models.DateField()
