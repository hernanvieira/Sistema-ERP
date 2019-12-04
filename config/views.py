from django.shortcuts import render
from tp_final.forms import ConfiguracionForm

def Configuracion (request):
    if request.method == 'POST':
        configuracion_form = ConfiguracionForm(request.POST)
        print(configuracion_form.errors)
        if configuracion_form.is_valid():
            configuracion = configuracion_form.save()
        else:
            messages.error(request, 'Ocurrió un error al tratar de establecer la configuracion')
    else:
        configuracion_form = ConfiguracionForm()
    return render(request, 'config/configuracion.html',{'configuracion_form':configuracion_form})
