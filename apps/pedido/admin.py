from django.contrib import admin
from .models import Pedido,Detalle,Estado_pedido
# Register your models here.
admin.site.register(Pedido)
admin.site.register(Detalle)
admin.site.register(Estado_pedido)
