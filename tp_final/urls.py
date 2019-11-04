"""tp_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.cliente.views import Home, Auditoria, Estadistica

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cliente/',include(('apps.cliente.urls','cliente')),name='cliente'),
    path('estado/',include(('apps.estado.urls','estado'))),
    path('material/',include(('apps.material.urls','material'))),
    path('pedido/',include(('apps.pedido.urls','pedido'))),
    path('prenda/',include(('apps.prenda.urls','prenda')),name='prenda'),
    path('home/', Home, name = 'index'),
    path('estadistica/', Estadistica, name = 'estadistica'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
