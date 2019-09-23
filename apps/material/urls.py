from django.urls import path
from .views import CrearTipo_material, ListarTipo_material, EditarTipo_material, EliminarTipo_material, CrearMaterial, ListarMaterial, EditarMaterial, EliminarMaterial, CrearUnidad_medida, ListarUnidad_medida, EditarUnidad_medida, EliminarUnidad_medida
from .views import CrearCompra, ListarCompra, EditarCompra, EliminarCompra

urlpatterns = [
            #URL Tipo_material
            path ('crear_tipo_material/',CrearTipo_material,name='crear_tipo_material'),
            path ('listar_tipo_material/',ListarTipo_material,name='listar_tipo_material'),
            path ('editar_tipo_material/<int:id_tipo_material>',EditarTipo_material,name='editar_tipo_material'),
            path ('eliminar_tipo_material/<int:id_tipo_material>',EliminarTipo_material,name='eliminar_tipo_material'),

            #URL Material
            path ('crear_material/',CrearMaterial,name='crear_material'),
            path ('listar_material/',ListarMaterial,name='listar_material'),
            path ('editar_material/<int:id_material>',EditarMaterial,name='editar_material'),
            path ('eliminar_material/<int:id_material>',EliminarMaterial,name='eliminar_material'),

            #URL Unidad_medida
            path ('crear_unidad_medida/',CrearUnidad_medida,name='crear_unidad_medida'),
            path ('listar_unidad_medida/',ListarUnidad_medida,name='listar_unidad_medida'),
            path ('editar_unidad_medida/<int:id_unidad>',EditarUnidad_medida,name='editar_unidad_medida'),
            path ('eliminar_unidad_medida/<int:id_unidad>',EliminarUnidad_medida,name='eliminar_unidad_medida'),

            #URL Compra
            path ('crear_compra/',CrearCompra,name='crear_compra'),
            path ('listar_compra/',ListarCompra,name='listar_compra'),
            path ('editar_compra/<int:id_compra>',EditarCompra,name='editar_compra'),
            path ('eliminar_compra/<int:id_compra>',EliminarCompra,name='eliminar_compra')
]
