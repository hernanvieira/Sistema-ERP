from django.db import models
from apps.cliente.models import Cliente
from apps.prenda.models import Prenda
# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Pedido (models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now=True)
    fecha_entrega = models.DateField(null = True, blank = True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True)
    entrega = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True, default = 0)
    seña = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank=True)
    prioridad_entrega = models.CharField(max_length=50, null = True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete = models.PROTECT)

class Detalle (models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    tiempo_prod_lote = models.IntegerField(null = True, blank = True)
    pedido = models.ForeignKey(Pedido, on_delete = models.PROTECT,null = True, blank = True)
    prenda = models.ForeignKey(Prenda, on_delete = models.PROTECT,null = True, blank = True)
