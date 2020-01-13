from django.urls import path
from .views import CrearPedido, MaterialesUtilizados, ListarPedido, ListaCompras, ListarPedido2, EditarPedido,VerPedido, EliminarPedido, CancelarPedido, VolverPedido, Auditoria, FinalizarPedido, EntregarPedido, NuevoPedido

urlpatterns = [
            #URL Pedido
            path ('crear_pedido/',CrearPedido,name='crear_pedido'),
            path ('nuevo_pedido/',NuevoPedido,name='nuevo_pedido'),
            path ('listar_pedido/',ListarPedido,name='listar_pedido'),
            path ('listar_pedido/<int:id_pedido>',ListarPedido2,name='listar_pedido2'),
            path ('editar_pedido/<int:id_pedido>',EditarPedido,name='editar_pedido'),
            path ('ver_pedido/<int:id_pedido>',VerPedido,name='ver_pedido'),
            path ('eliminar_pedido/<int:id_pedido>',EliminarPedido,name='eliminar_pedido'),
            path ('volver_pedido/<int:id_pedido>',VolverPedido,name='volver_pedido'),
            path ('cancelar_pedido/<int:id_pedido>',CancelarPedido,name='cancelar_pedido'),
            path ('finalizar_pedido/<int:id_pedido>',FinalizarPedido,name='finalizar_pedido'),
            path ('entregar_pedido/<int:id_pedido>',EntregarPedido,name='entregar_pedido'),
            path ('materiales_utilizados/<int:id_pedido>',MaterialesUtilizados,name='materiales_utilizados'),
            path('auditoria/', Auditoria, name = 'auditoria'),
            path ('lista_compras/',ListaCompras,name='lista_compras')
]
