from django.urls import path
from .views import CrearPedido, ListarPedido, EditarPedido,VerPedido, EliminarPedido, CancelarPedido, VolverPedido, Auditoria, RegistrarEntrega

urlpatterns = [
            #URL Pedido
            path ('crear_pedido/',CrearPedido,name='crear_pedido'),
            path ('listar_pedido/',ListarPedido,name='listar_pedido'),
            path ('editar_pedido/<int:id_pedido>',EditarPedido,name='editar_pedido'),
            path ('ver_pedido/<int:id_pedido>',VerPedido,name='ver_pedido'),
            path ('eliminar_pedido/<int:id_pedido>',EliminarPedido,name='eliminar_pedido'),
            path ('volver_pedido/<int:id_pedido>',VolverPedido,name='volver_pedido'),
            path ('cancelar_pedido/<int:id_pedido>',CancelarPedido,name='cancelar_pedido'),
            path ('registrar_entrega/<int:id_pedido>',RegistrarEntrega,name='registrar_entega'),
            path('auditoria/', Auditoria, name = 'auditoria')
]
