from django.db import models
from apps.cliente.models import Cliente
from apps.prenda.models import Prenda
from apps.material.models import Material, Tipo_material
from django.core.validators import MaxValueValidator, MinValueValidator

#from apps.usuario.models import CustomUser

from simple_history.models import HistoricalRecords

#Se crean las clases de acuerdo al diagrama de clases

class Pedido (models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now=True)
    fecha_entrega = models.DateField(null = True, blank = True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True, validators=[MinValueValidator(0.00)], default=0)
    entrega = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True, default = 0, validators=[MinValueValidator(0.00)])
    seña = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True, validators=[MinValueValidator(0.00)])
    prioridad_entrega = models.CharField(max_length=50, null = True, blank=True, default = 2)
    cancelado = models.BooleanField(default = False)
    cliente = models.ForeignKey(Cliente, on_delete = models.PROTECT)
    puntaje = models.CharField(max_length=50, null = True, blank = True, default = 2)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id_pedido)

class Detalle (models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    tiempo_prod_lote = models.PositiveIntegerField(null = True, blank = True, default=0)
    pedido = models.ForeignKey(Pedido, on_delete = models.PROTECT,null = True, blank = True)
    prenda = models.ForeignKey(Prenda, on_delete = models.PROTECT,null = True, blank = True)

class Entregas (models.Model):
    id_entrega = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], default=0)
    pedido = models.ForeignKey(Pedido, on_delete = models.PROTECT)
    fecha_entrega = models.DateField(auto_now=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True, default = 0, validators=[MinValueValidator(0.00)])
    #usuario = models.ForeignKey(CustomUser, on_delete = models.PROTECT, null = True)

class Faltante (models.Model):
    id_faltante = models.AutoField(primary_key=True)
    tipo_material = models.ForeignKey(Tipo_material, on_delete=models.PROTECT)
    material =  models.ForeignKey(Material, on_delete=models.PROTECT)
    faltante = models.PositiveIntegerField(default=0)
    prenda = models.ForeignKey(Prenda, on_delete=models.PROTECT)
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Faltante'
        verbose_name_plural = 'Faltantes'
        ordering = ['id_faltante']
