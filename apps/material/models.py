from django.db import models

# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases
class Unidad_medida (models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Unidad_medida'
        verbose_name_plural = 'Unidad_medida'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Tipo_material (models.Model):
    id_tipo_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    unidad_medida = models.ForeignKey(Unidad_medida,on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipos de materiales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Material (models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()
    tipo_material = models.ForeignKey(Tipo_material, on_delete=models.PROTECT)
    stock_minimo = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre + ' ' + self.color

class Compra (models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    material = models.ManyToManyField(Material)
