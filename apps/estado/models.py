from django.db import models
from apps.pedido.models import Pedido
from apps.pedido.models import Detalle
# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Estado (models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)

class Estado_pedido (models.Model):
    id_estado_pedido = models.AutoField(primary_key=True)
    fecha = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

class Estado_lote (models.Model):
    id_estado_lote = models.AutoField(primary_key=True)
    fecha = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    detalle = models.ForeignKey(Detalle, on_delete = models.CASCADE)
