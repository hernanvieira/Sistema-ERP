from django.urls import path
from .views import CrearComponente, ListarComponente, EditarComponente, EliminarComponente , CrearTipo_prenda, ListarTipo_prenda, EditarTipo_prenda, EliminarTipo_prenda, VerTipo_prenda
from .views import CrearPrenda, ListarPrenda, EditarPrenda, EliminarPrenda, AsignarMaterial, VolverPrenda, EditarIngrediente, EliminarIngrediente
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
            path ('eliminar_tipo_prenda/<int:id_tipo_prenda>',EliminarTipo_prenda,name='eliminar_tipo_prenda'),
            path ('ver_tipo_prenda/<int:id_tipo_prenda>',VerTipo_prenda,name='ver_tipo_prenda'),

            #URL prenda
            path ('crear_prenda/<int:id_pedido>',CrearPrenda,name='crear_prenda'),
            path ('listar_prenda/',ListarPrenda,name='listar_prenda'),
            path ('editar_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',EditarPrenda,name='editar_prenda'),
            path ('eliminar_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',EliminarPrenda,name='eliminar_prenda'),
            path ('volver_prenda/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',VolverPrenda,name='volver_prenda'),
            path ('asignar_material/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',AsignarMaterial,name='asignar_material'),
            path ('editar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',EditarIngrediente,name='editar_ingrediente'),
            path ('eliminar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',EliminarIngrediente,name='eliminar_ingrediente')

            ]
