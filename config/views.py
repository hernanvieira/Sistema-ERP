from django.shortcuts import render
from tp_final.forms import ConfiguracionForm, ConfiguracionMensajeForm
from config.models import Configuracion, ConfiguracionMensaje
from django.contrib import messages
from apps.pedido.models import Pedido,Detalle_envio

def configuracion (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    if request.method == 'POST':
        configuracion_form = ConfiguracionForm(request.POST)
        if configuracion_form.is_valid():
            configuracion = configuracion_form.save()
            messages.success(request, 'Se pudo establecer la configuración correctamente')
        else:
            messages.error(request, 'Ocurrió un error al tratar de establecer la configuración')
    else:
        configuracion_actual = Configuracion.objects.all().last()
        configuracion_form = ConfiguracionForm(instance=configuracion_actual)

    return render(request, 'config/configuracion.html',{'envios_not':envios_not,'envio_count':envio_count, 'configuracion_form':configuracion_form})

def configuracionMensaje (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    if request.method == 'POST':
        configuracion_mensaje_form = ConfiguracionMensajeForm(request.POST)
        print(configuracion_mensaje_form.errors)
        if configuracion_mensaje_form.is_valid():
            configuracion = configuracion_mensaje_form.save()
            messages.success(request, 'Se logró establecer la configuración correctamente')
        else:
            messages.error(request, 'Ocurrió un error al tratar de establecer la configuracion')
    else:
        configuracion_actual = ConfiguracionMensaje.objects.all().last()
        configuracion_mensaje_form = ConfiguracionMensajeForm(instance=configuracion_actual)
    return render(request, 'config/configuracion_mensaje.html',{'envios_not':envios_not,'envio_count':envio_count, 'configuracion_mensaje_form':configuracion_mensaje_form})
