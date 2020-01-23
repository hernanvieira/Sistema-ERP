from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import ClienteForm
from .models import Cliente
from apps.pedido.models import Pedido
from django.core.exceptions import *
from django.contrib import messages
from config.models import Configuracion
from apps.pedido.models import Faltante
from apps.material.models import Material

from django.db.models import Sum

import poplib # Recibir correos

from apps.prenda.models import Tipo_prenda, Prenda
from apps.estado.models import Estado_pedido


# Create your views here.

#Pagina de inicio
def Home(request):
    pedidos = Pedido.objects.all()
    reporte = Configuracion.objects.all().last()

    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux
    print(pedidos[0].pedido)

    lista = Faltante.objects.values('material').order_by('material').annotate(sum=Sum('faltante')) #Obtengo un queryset con la suma de faltante agrupado por cada material, solo me trae el id

    #Creo una lista para guardar los objetos de cada material
    materiales=[]
    #Obtengo los objetos y los agrego a la lista
    for i in range(len(lista)):
        material = Material.objects.get(id_material = lista[i]['material'])
        materiales.append(material)

    #Intercambio los id de cada material por el objeto en si
    for i in range(len(materiales)):
        lista[i]['material'] = materiales[i]

    return render(request, 'index.html',{'reporte':reporte,'pedidos':pedidos, 'lista':lista})

#Pagina de estadisticas
def Estadistica(request):
    lista_chart = []

    tipo_prendas_list = Tipo_prenda.objects.all()
    for tipo_prenda in tipo_prendas_list:
        diccionario = {
        'prenda':tipo_prenda.nombre,
        'valor':Prenda.objects.filter(tipo_prenda = tipo_prenda).count()
        }
        lista_chart.append(diccionario)
    print(lista_chart)
    return render(request, 'estadistica.html',{'lista_chart':lista_chart})

#Crear un cliente
def CrearCliente (request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        print("ALTO ERROR WACHO")
        print(cliente_form.errors)
        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, 'Sea agregó correctamente el cliente')
            return ClienteHome(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de agregar el cliente')
    else:
        cliente_form = ClienteForm()
    return render(request, 'cliente/crear_cliente.html',{'cliente_form':cliente_form})

#Editar un cliente
def VerCliente (request,dni):
    try:
        cliente_form=None
        cliente = Cliente.objects.get(dni=dni)
        pedidos = Pedido.objects.filter(cliente = cliente).exclude(confirmado = False)
        if request.method=='GET':
            cliente_form=ClienteForm(instance=cliente)
        else:
            cliente_form=ClienteForm(request.POST, instance=cliente)
            if cliente_form.is_valid():
                cliente_form.save()
            return redirect('cliente:cliente_home')
    except ObjectDoesNotExist as e:
        error = e
    return render(request, 'cliente/ver_cliente.html',{'pedidos':pedidos, 'cliente':cliente ,'cliente_form':cliente_form})

#Listar todos los clientes
def ListarCliente (request):
    clientes = Cliente.objects.all().exclude(activo = False)
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
        cliente.activo = False
        cliente.save()
        messages.warning(request, 'Se eliminó el cliente')
        clientes = Cliente.objects.all().exclude(activo = False)
        return render(request,'cliente/index_cliente.html',{'cliente':cliente,'clientes':clientes})
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el cliente')
    clientes = Cliente.objects.all().exclude(activo = False)
    return render(request,'cliente/index_cliente.html',{'cliente':cliente,'clientes':clientes})

def ClienteHome(request):
    clientes = Cliente.objects.all().exclude(activo = False)
    cliente_form = ClienteForm()
    reporte = Configuracion.objects.all().last()
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)

        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, 'Sea agregó correctamente el cliente')
            return render (request, 'cliente/index_cliente.html',{'clientes':clientes})
        else:
            errores = cliente_form.errors.values() #Obtengo los valores devueltos en el diccionario
            errores = list(errores) #Los casteo a lista porque no es iterable
            for error in errores:
                error = str(error) #Casteo el error a str (solo para eliminar el PUNTITO del <li>)
                error = error.replace('<ul class="errorlist"><li>', '') #Borro la parte esta jaja
                error = error.replace('</li></ul>', '') # y la parte esta jiji
                messages.error(request,error) # PAAAaaaaa un mensajito de error to lindo
            cliente_form = ClienteForm(request.POST)
    else:
        cliente_form = ClienteForm()
    return render (request, 'cliente/index_cliente.html',{'reporte':reporte,'clientes':clientes,'cliente_form':cliente_form})

#Pagina de auditoria
def Auditoria(request):
    auditoria =  Cliente.history.all()
    return render(request, 'auditoria_cliente.html',{'auditoria':auditoria})
