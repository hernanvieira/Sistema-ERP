from django.urls import path
from .views import EliminarUsuario

from django.contrib.auth.decorators import login_required

urlpatterns = [
            #URL Medida
            path ('eliminar_usuario/<int:id>',login_required(EliminarUsuario),name='eliminar_usuario')
            ]
