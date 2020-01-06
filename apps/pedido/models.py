from django.db import models
from apps.cliente.models import Cliente
from apps.prenda.models import Prenda
from django.core.validators import MaxValueValidator, MinValueValidator

from simple_history.models import HistoricalRecords
# Create your models here.
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
