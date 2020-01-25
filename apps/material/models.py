from django.db import models

from apps.usuario.models import customuser


# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases
class Unidad_medida (models.Model):
    id_unidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique = True)
    descripcion = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Unidad_medida'
        verbose_name_plural = 'Unidad_medida'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = (self.nombre).upper()
        self.descripcion = (self.descripcion).upper()
        return super(Unidad_medida, self).save(*args, **kwargs)

class Tipo_material (models.Model):
    id_tipo_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique = True)
    unidad_medida = models.ForeignKey(Unidad_medida,on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Tipo de Material'
        verbose_name_plural = 'Tipos de materiales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = (self.nombre).upper()
        return super(Tipo_material, self).save(*args, **kwargs)


class Material (models.Model):
    id_material = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=50, default='#ffffff')
    stock = models.IntegerField(default=0)
    tipo_material = models.ForeignKey(Tipo_material, on_delete=models.PROTECT)
    stock_minimo = models.PositiveIntegerField(default=0)
    tiempo_reposicion = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = (self.nombre).upper()
        self.color = (self.color).upper()
        return super(Material, self).save(*args, **kwargs)

class Compra (models.Model):
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateField()
    cantidad = models.PositiveIntegerField()
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    usuario = models.ForeignKey(customuser, on_delete = models.PROTECT, null = True)
