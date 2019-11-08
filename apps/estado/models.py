from django.db import models
from apps.pedido.models import Pedido
from apps.pedido.models import Detalle
# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Estado (models.Model):
    id_estado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        ordering = ['id_estado']

    def __str__(self):
        return str(self.nombre)


class Estado_pedido (models.Model):
    id_estado_pedido = models.AutoField(primary_key=True)
    fecha = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Estado_pedido'
        verbose_name_plural = 'Estados_pedido'
        ordering = ['id_estado_pedido']

    def __str__(self):
        return str(self.estado)

class Estado_lote (models.Model):
    id_estado_lote = models.AutoField(primary_key=True)
    fecha = models.DateField()
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    detalle = models.ForeignKey(Detalle, on_delete = models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Estado_lote'
        verbose_name_plural = 'Estados_lote'
        ordering = ['id_estado_lote']

    def __str__(self):
        return str(self.estado)
