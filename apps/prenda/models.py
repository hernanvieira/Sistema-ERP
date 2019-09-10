from django.db import models

# Create your models here.
#Se crean las clases de acuerdo con diagrama de clases

class Prenda (models.Model):
    id_prenda = models.AutoField(primary_key = True)
    talle = models.IntegerField()
    tiempo_prod_prenda = models.IntegerField()
    activo = models.BooleanField()

class Tipo_prenda (models.Model):
    id_tipo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

class Componente (models.Model):
    id_componente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank = False, null = False)

class Ingrediente (models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
