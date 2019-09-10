from django.db import models

# Create your models here.
#Se crean las clases de acuerdo al diagrama de clases

class Pedido (models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField()
    fecha_entrega = models.DateField()
    precio_total = models.DecimalField()
    entrega = models.DecimalField()
    seña = models.DecimalField()
    estado = models.CharField(max_length=100)
    prioridad_entrega = models.CharField(max_length=50)
    activo = models.BooleanField()

class Detalle (models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    tiempo_prod_lote = models.IntegerField()
    activo = models.BooleanField()

class Estado_pedido (models.Model):
    fecha = models.DateField()
    
