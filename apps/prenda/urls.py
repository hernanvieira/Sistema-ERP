from django.urls import path
from .views import CrearMedida, ListarMedida, EditarMedida, EliminarMedida , CrearTipo_prenda, ListarTipo_prenda, EditarTipo_prenda, EliminarTipo_prenda, VerTipo_prenda
from .views import CrearPrenda, ListarPrenda, EditarPrenda, VerPrenda, EliminarPrenda, AsignarMaterial, CalcularDisponibilidad, AsignarMedida, VolverPrenda, EditarIngrediente, EliminarIngrediente, MostrarUnidad, TiempoProdPrenda

from django.contrib.auth.decorators import login_required

urlpatterns = [
            #URL Medida
            path ('crear_medida/',login_required(CrearMedida),name='crear_medida'),
            path ('listar_medida/',login_required(ListarMedida),name='listar_medida'),
            path ('editar_medida/<int:id_medida>',login_required(EditarMedida),name='editar_medida'),
            path ('eliminar_medida/<int:id_medida>',login_required(EliminarMedida),name='eliminar_medida'),

            #URL Tipo_prenda
            path ('crear_tipo_prenda/',login_required(CrearTipo_prenda),name='crear_tipo_prenda'),
            path ('listar_tipo_prenda/',login_required(ListarTipo_prenda),name='listar_tipo_prenda'),
            path ('editar_tipo_prenda/<int:id_tipo_prenda>',login_required(EditarTipo_prenda),name='editar_tipo_prenda'),
            path ('eliminar_tipo_prenda/<int:id_tipo_prenda>',login_required(EliminarTipo_prenda),name='eliminar_tipo_prenda'),
            path ('ver_tipo_prenda/<int:id_tipo_prenda>',login_required(VerTipo_prenda),name='ver_tipo_prenda'),

            #URL prenda
            path ('crear_prenda/<int:id_pedido>',login_required(CrearPrenda),name='crear_prenda'),
            path ('listar_prenda/',login_required(ListarPrenda),name='listar_prenda'),
            path ('editar_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(EditarPrenda),name='editar_prenda'),
            path ('ver_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(VerPrenda),name='ver_prenda'),
            path ('eliminar_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(EliminarPrenda),name='eliminar_prenda'),
            path ('volver_prenda/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(VolverPrenda),name='volver_prenda'),
            path ('asignar_material/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(AsignarMaterial),name='asignar_material'),
            path ('calcular_disponibilidad/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(CalcularDisponibilidad),name='calcular_disponibilidad'),
            path ('asignar_medida/<int:id_prenda>/<int:id_detalle>/<int:id_pedido>',login_required(AsignarMedida),name='asignar_medida'),
            path ('editar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',login_required(EditarIngrediente),name='editar_ingrediente'),
            path ('eliminar_material/<int:id_ingrediente>/<int:id_pedido>/<int:id_detalle>/<int:id_prenda>',login_required(EliminarIngrediente),name='eliminar_ingrediente'),
            path ('mostrar_unidad/',login_required(MostrarUnidad),name='mostrar_unidad'),
            path ('tiempo_prod/',login_required(TiempoProdPrenda),name='tiempo_prod')
            ]
