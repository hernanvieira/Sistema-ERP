from django.db import models
from apps.material.models import Material
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
#Se crean las clases de acuerdo con diagrama de clases
class Componente (models.Model):
    id_componente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank = False, null = False, unique = True)

    class Meta:
        verbose_name = 'Componente'
        verbose_name_plural = 'Componentes'
        ordering = ['id_componente']

    def __str__(self):
        return self.nombre

class Tipo_prenda (models.Model):
    id_tipo_prenda = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique = True)
    componente = models.ManyToManyField(Componente)

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

    # def __str__(self):
    #     return self.id_prenda

class Ingrediente (models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT,null = True, blank = True)
    # componente = models.ForeignKey(Componente, on_delete=models.PROTECT,null = True, blank = True)
    material =  models.ForeignKey(Material, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingrediente'
        ordering = ['id_ingrediente']

    def __str__(self):
        return str(self.id_ingrediente)
