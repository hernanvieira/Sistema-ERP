from django.db import models
from apps.material.models import Material
# Create your models here.
#Se crean las clases de acuerdo con diagrama de clases
class Componente (models.Model):
    id_componente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank = False, null = False)

class Tipo_prenda (models.Model):
    id_tipo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    componente = models.ManyToManyField(Componente)

class Prenda (models.Model):
    id_prenda = models.AutoField(primary_key = True)
    talle = models.IntegerField()
    tiempo_prod_prenda = models.IntegerField()
    activo = models.BooleanField()
    tipo_prenda = models.ForeignKey(Tipo_prenda, on_delete=models.CASCADE)

class Ingrediente (models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE)
    componente = models.ForeignKey(Componente, on_delete=models.CASCADE)
    material =  models.ForeignKey(Material, on_delete=models.CASCADE)
