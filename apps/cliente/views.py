from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import ClienteForm
from .models import Cliente
from django.core.exceptions import *
from django.contrib import messages


# Create your views here.

#Pagina de inicio
def Home(request):
    return render(request, 'index.html')

#Pagina de auditoria
def Auditoria(request):
    auditoria =  Cliente.history.all()
    return render(request, 'auditoria.html',{'auditoria':auditoria})

#Crear un cliente
def CrearCliente (request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            print("ENTRASSEE")
            cliente_form.save()
            messages.success(request, 'Sea agregó correctamente el cliente')
            return ClienteHome(request)
        else:
            print("ERORAROSOO")
            messages.error(request, 'Ocurrió un error al tratar de agregar el cliente')
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
    return render(request, 'cliente/crear_cliente.html',{'cliente_form':cliente_form})

#Eliminar un cliente
def EliminarCliente (request,dni):
    cliente = get_object_or_404(Cliente,dni=dni)
    try:
        cliente.delete()
        messages.warning(request, 'Se eliminó el cliente')
        clientes = Cliente.objects.all()
        return render(request,'cliente/index_cliente.html',{'cliente':cliente,'clientes':clientes})
    except Exception as e:
        print("por k entra aca?")
        messages.error(request, 'Ocurrió un error al tratar de eliminar el cliente')
    clientes = Cliente.objects.all()
    return render(request,'cliente/index_cliente.html',{'cliente':cliente,'clientes':clientes})

def ClienteHome(request):
    clientes = Cliente.objects.all()
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, 'Sea agregó correctamente el cliente')
            print("Entra")
            return render (request, 'cliente/index_cliente.html',{'clientes':clientes})
        else:
            print("Entra aca tambien")
            messages.error(request, 'Ocurrió un error al tratar de agregar el cliente')
            cliente_form = ClienteForm()
    else:
        cliente_form = ClienteForm()
    return render (request, 'cliente/index_cliente.html',{'clientes':clientes,'cliente_form':cliente_form})
