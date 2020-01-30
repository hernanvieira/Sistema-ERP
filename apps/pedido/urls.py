from django.urls import path
from .views import CrearPedido, MaterialesUtilizados,ConfirmarEntrega, ListarPedido, ListaCompras, ListarPedido2, EditarPedido,VerPedido, EliminarPedido, CancelarPedido, VolverPedido, Auditoria, FinalizarPedido, EntregarPedido, NuevoPedido

from django.contrib.auth.decorators import login_required

urlpatterns = [
            #URL Pedido
            path ('crear_pedido/',login_required(CrearPedido),name='crear_pedido'),
            path ('nuevo_pedido/',login_required( NuevoPedido),name='nuevo_pedido'),
            path ('listar_pedido/',login_required(ListarPedido),name='listar_pedido'),
            path ('listar_pedido/<int:id_pedido>',login_required(ListarPedido2),name='listar_pedido2'),
            path ('editar_pedido/<int:id_pedido>',login_required(EditarPedido),name='editar_pedido'),
            path ('ver_pedido/<int:id_pedido>',login_required(VerPedido),name='ver_pedido'),
            path ('eliminar_pedido/<int:id_pedido>',login_required(EliminarPedido),name='eliminar_pedido'),
            path ('volver_pedido/<int:id_pedido>',login_required(VolverPedido),name='volver_pedido'),
            path ('cancelar_pedido/<int:id_pedido>',login_required(CancelarPedido),name='cancelar_pedido'),
            path ('finalizar_pedido/<int:id_pedido>',login_required(FinalizarPedido),name='finalizar_pedido'),
            path ('entregar_pedido/<int:id_pedido>',login_required(EntregarPedido),name='entregar_pedido'),
            path ('materiales_utilizados/<int:id_pedido>',login_required(MaterialesUtilizados),name='materiales_utilizados'),
            path('auditoria/', login_required(Auditoria), name = 'auditoria'),
            path ('lista_compras/',login_required(ListaCompras),name='lista_compras'),
            path ('confirmar_entrega/<int:id_pedido>/<int:id_cliente>',ConfirmarEntrega,name='confirmar_entrega'),
]
