from django.urls import path
from .views import CrearCliente

urlpatterns = [
        path ('crear_cliente/', CrearCliente, name='crear_cliente')
]
