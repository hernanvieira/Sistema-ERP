from django.urls import path
from .views import CrearTipo_material, ListarTipo_material, EditarTipo_material, EliminarTipo_material, CrearMaterial, ListarMaterial, EditarMaterial, EliminarMaterial

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
            path ('eliminar_material/<int:id_material>',EliminarMaterial,name='eliminar_material')
]
