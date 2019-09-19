from django.urls import path
from .views import CrearComponente, ListarComponente, EditarComponente, EliminarComponente , CrearTipo_prenda, ListarTipo_prenda, EditarTipo_prenda, EliminarTipo_prenda

urlpatterns = [
            #URL Componente
            path ('crear_componente/',CrearComponente,name='crear_componente'),
            path ('listar_componente/',ListarComponente,name='listar_componente'),
            path ('editar_componente/<int:id_componente>',EditarComponente,name='editar_componente'),
            path ('eliminar_componente/<int:id_componente>',EliminarComponente,name='eliminar_componente'),

            #URL Tipo_prenda
            path ('crear_tipo_prenda/',CrearTipo_prenda,name='crear_tipo_prenda'),
            path ('listar_tipo_prenda/',ListarTipo_prenda,name='listar_tipo_prenda'),
            path ('editar_tipo_prenda/<int:id_tipo_prenda>',EditarTipo_prenda,name='editar_tipo_prenda'),
            path ('eliminar_tipo_prenda/<int:id_tipo_prenda>',EliminarTipo_prenda,name='eliminar_tipo_prenda')
]
