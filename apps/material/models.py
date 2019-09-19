from django.db import models

# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases
class Unidad_medida (models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

class Tipo_material (models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField()
    unidad_medida = models.ForeignKey(Unidad_medida,on_delete=models.CASCADE)

class Material (models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    tipo_material = models.ForeignKey(Tipo_material, on_delete=models.CASCADE)

class Compra (models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    material = models.ManyToManyField(Material)