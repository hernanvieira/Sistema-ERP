from django.shortcuts import render,redirect
from tp_final.forms import ClienteForm
# Create your views here.
#
def Home(request):
    return render(request, 'index.html')

def CrearCliente (request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            return redirect('index')
    else:
        cliente_form = ClienteForm()
    return render(request, 'cliente/crear_cliente.html',{'cliente_form':cliente_form})
