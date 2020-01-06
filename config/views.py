from django.shortcuts import render
from tp_final.forms import ConfiguracionForm, ConfiguracionMensajeForm
from config.models import Configuracion, ConfiguracionMensaje

def configuracion (request):
    if request.method == 'POST':
        configuracion_form = ConfiguracionForm(request.POST)
        if configuracion_form.is_valid():
            configuracion = configuracion_form.save()
        else:
            messages.error(request, 'Ocurrió un error al tratar de establecer la configuracion')
    else:
        configuracion_actual = Configuracion.objects.all().last()
        configuracion_form = ConfiguracionForm(instance=configuracion_actual)

    return render(request, 'config/configuracion.html',{'configuracion_form':configuracion_form})

def configuracionMensaje (request):
    if request.method == 'POST':
        configuracion_mensaje_form = ConfiguracionMensajeForm(request.POST)
        print(configuracion_mensaje_form.errors)
        if configuracion_mensaje_form.is_valid():
            configuracion = configuracion_mensaje_form.save()
        else:
            messages.error(request, 'Ocurrió un error al tratar de establecer la configuracion')
    else:
        configuracion_actual = ConfiguracionMensaje.objects.all().last()
        configuracion_mensaje_form = ConfiguracionMensajeForm(instance=configuracion_actual)
    return render(request, 'config/configuracion_mensaje.html',{'configuracion_mensaje_form':configuracion_mensaje_form})
