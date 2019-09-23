from django.db import models
from apps.cliente.models import Cliente
from apps.prenda.models import Prenda
# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Pedido (models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(auto_now=True)
    fecha_entrega = models.DateField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    entrega = models.DecimalField(max_digits=10, decimal_places=2)
    seña = models.DecimalField(max_digits=10, decimal_places=2)
    prioridad_entrega = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)

class Detalle (models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    tiempo_prod_lote = models.IntegerField()
    pedido = models.ForeignKey(Pedido, on_delete = models.CASCADE)
    prenda = models.ForeignKey(Prenda, on_delete = models.CASCADE)
