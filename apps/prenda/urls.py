from django.urls import path
from .views import CrearMedida, ListarMedida, EditarMedida, EliminarMedida , CrearTipo_prenda, ListarTipo_prenda, EditarTipo_prenda, EliminarTipo_prenda, VerTipo_prenda
from .views import CrearPrenda, ListarPrenda, EditarPrenda, EliminarPrenda, AsignarMaterial, AsignarMedida, VolverPrenda, EditarIngrediente, EliminarIngrediente, MostrarUnidad, TiempoProdPrenda
urlpatterns = [
            #URL Medida
            path ('crear_medida/',CrearMedida,name='crear_medida'),
            path ('listar_medida/',ListarMedida,name='listar_medida'),
            path ('editar_medida/<int:id_medida>',EditarMedida,name='editar_medida'),
            path ('eliminar_medida/<int:id_medida>',EliminarMedida,name='eliminar_medida'),

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
            path ('volver_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',VolverPrenda,name='volver_prenda'),
            path ('asignar_material/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',AsignarMaterial,name='asignar_material'),
            path ('asignar_medida/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',AsignarMedida,name='asignar_medida'),
            path ('editar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',EditarIngrediente,name='editar_ingrediente'),
            path ('eliminar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',EliminarIngrediente,name='eliminar_ingrediente'),
            path ('mostrar_unidad/',MostrarUnidad,name='mostrar_unidad'),
            path ('tiempo_prod/',TiempoProdPrenda,name='tiempo_prod'),
            ]
