from django.urls import path
from .views import CrearCliente, ListarCliente, EditarCliente, EliminarCliente, ClienteHome, Auditoria, VerAuditoria, VerCliente

from django.contrib.auth.decorators import login_required

urlpatterns = [
        path ('crear_cliente/',login_required(CrearCliente),name='crear_cliente'),
        path ('listar_cliente/',login_required(ListarCliente),name='listar_cliente'),
        path ('editar_cliente/<int:dni>',login_required(EditarCliente),name='editar_cliente'),
        path ('eliminar_cliente/<int:dni>',login_required(EliminarCliente),name='eliminar_cliente'),
        path ('cliente_home/',login_required(ClienteHome),name='cliente_home'),
        path('ver_cliente/<int:dni>',login_required(VerCliente), name = 'ver_cliente'),
        path('auditoria/', login_required(Auditoria), name = 'auditoria'),
        path('ver_auditoria/<int:pk>/<int:id_history>', login_required(VerAuditoria), name = 'ver_auditoria')
]
