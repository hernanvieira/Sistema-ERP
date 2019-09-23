from django.urls import path
from .views import CrearPedido, ListarPedido, EditarPedido, EliminarPedido

urlpatterns = [
            #URL Pedido
            path ('crear_pedido/',CrearPedido,name='crear_pedido'),
            path ('listar_pedido/',ListarPedido,name='listar_pedido'),
            path ('editar_pedido/<int:id_pedido>',EditarPedido,name='editar_pedido'),
            path ('eliminar_pedido/<int:id_pedido>',EliminarPedido,name='eliminar_pedido')
]
