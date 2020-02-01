from rest_framework import serializers
from .models import *
from apps.cliente.models import Cliente

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['id_pedido']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['dni','apellido','nombre']

class Detalle_envioSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer()
    cliente = ClienteSerializer()
    class Meta:
        model = Detalle_envio
        fields = ['fecha_pedido','pedido','cliente']
