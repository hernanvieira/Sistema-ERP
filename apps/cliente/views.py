from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import ClienteForm
from .models import Cliente
from django.core.exceptions import *
from django.contrib import messages
# Create your views here.

#Pagina de inicio
def Home(request):
    return render(request, 'index.html')
#Crear un cliente
def CrearCliente (request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        print(cliente_form.errors)
        if cliente_form.is_valid():
            cliente_form.save()
            return ClienteHome(request)
    else:
        cliente_form = ClienteForm()
    return render(request, 'cliente/crear_cliente.html',{'cliente_form':cliente_form})
#Listar todos los clientes
def ListarCliente (request):
    clientes = Cliente.objects.all()
    return render(request,'cliente/listar_cliente.html',{'clientes':clientes})
#Editar un cliente
def EditarCliente (request,dni):
    try:
        error = None
        cliente_form=None
        cliente = Cliente.objects.get(dni=dni)
        if request.method=='GET':
            cliente_form=ClienteForm(instance=cliente)
        else:
            cliente_form=ClienteForm(request.POST, instance=cliente)
            if cliente_form.is_valid():
                cliente_form.save()
            return redirect('cliente:cliente_home')
    except ObjectDoesNotExist as e:
        error = e
    return render(request, 'cliente/crear_cliente.html',{'cliente_form':cliente_form, 'error':error})

#Eliminar un cliente
def EliminarCliente (request,dni):
    cliente = get_object_or_404(Cliente,dni=dni)
    try:
        cliente.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el cliente')
    clientes = Cliente.objects.all()
    return render(request,'cliente/index_cliente.html',{'cliente':cliente,'clientes':clientes})

def ClienteHome(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            return ClienteHome(request)
    else:
        cliente_form = ClienteForm()
    return render (request, 'cliente/index_cliente.html',{'clientes':clientes,'cliente_form':cliente_form})
