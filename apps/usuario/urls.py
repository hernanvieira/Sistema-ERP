from django.urls import path
from .views import EliminarUsuario
urlpatterns = [
            #URL Medida
            path ('eliminar_usuario/<int:id>',EliminarUsuario,name='eliminar_usuario')
            ]
