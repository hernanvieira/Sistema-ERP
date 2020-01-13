from django.db import models

from apps.material.models import Material, Unidad_medida, Tipo_material
from django.core.validators import MaxValueValidator, MinValueValidator


class Medida (models.Model):
    id_medida = models.AutoField(primary_key=True)
    nombre_medida = models.CharField(max_length=100, unique = True)
    unidad_medida =  models.ForeignKey(Unidad_medida, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medida'
        ordering = ['id_medida']

    def __str__(self):
        return str(self.nombre_medida)

class Tipo_prenda (models.Model):
    id_tipo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique = True)
    medida = models.ManyToManyField(Medida)

    class Meta:
        verbose_name = 'Tipo de Prenda'
        verbose_name_plural = 'Tipos de Prenda'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Prenda (models.Model):
    id_prenda = models.AutoField(primary_key = True)
    talle = models.PositiveIntegerField()
    tiempo_prod_prenda = models.PositiveIntegerField()
    tipo_prenda = models.ForeignKey(Tipo_prenda, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    imagen = models.ImageField(upload_to = "prendas", null = True, blank = True)

    class Meta:
        verbose_name = 'Prenda'
        verbose_name_plural = 'Prenda'
        ordering = ['id_prenda']

    def __str__(self):
        return str(self.id_prenda)

class Medida_prenda (models.Model):
    id_medida_prenda = models.AutoField(primary_key=True)
    valor = models.PositiveIntegerField(default = 0, null = True, blank = True)
    medida = models.ForeignKey(Medida, on_delete=models.PROTECT, null = True, blank = True)
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT, null = True, blank = True)

    class Meta:
        verbose_name = 'Medida_prenda'
        verbose_name_plural = 'Medida_prenda'
        ordering = ['id_medida_prenda']

class Ingrediente (models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT,null = True, blank = True)
    material =  models.ForeignKey(Material, on_delete=models.PROTECT)
    cantidadxdetalle = models.PositiveIntegerField(default=0)
    disponibilidad = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingrediente'
        ordering = ['id_ingrediente']

    def __str__(self):
        return str(self.id_ingrediente)
