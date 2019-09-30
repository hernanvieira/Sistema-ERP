from django.shortcuts import render, redirect
from tp_final.forms import PedidoForm, DetalleForm, PrendaForm, IngredienteForm, DetalleForm, ClienteForm
from .models import Pedido, Detalle
from apps.prenda.models import Prenda
from apps.prenda.views import CrearPrenda
from django.core.exceptions import ObjectDoesNotExist
from tp_final import urls
#Crear un pedido
def CrearPedido (request):
    if request.method == 'POST':
        print(request.POST)
        pedido_form = PedidoForm(request.POST)
        prenda_form = PrendaForm(request.POST)
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid() :
            cliente_form.save()
        if pedido_form.is_valid():
            pedido = pedido_form.save()
            id_pedido = pedido.id_pedido
            return redirect('/prenda/crear_prenda/'+str(id_pedido))
    else:
        pedido_form = PedidoForm()
        cliente_form = ClienteForm()
    return render(request, 'pedido/crear_pedido.html',{'pedido_form':pedido_form, 'cliente_form':cliente_form})
#Listar todos los pedidoes
def ListarPedido (request):
    pedidos = Pedido.objects.all()
    return render(request,'pedido/listar_pedido.html',{'pedidos':pedidos})

#Volver al pedido
def VolverPedido (request,id_pedido,id_detalle):
    try:
        detalles = None
        error = None
        pedido_form=None
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        pedido_id = pedido.id_pedido
        detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
        print(detalles)
        if request.method=='GET':
            pedido_form=PedidoForm(instance=pedido)
        else:
            pedido_form=PedidoForm(request.POST, instance=pedido)
            if pedido_form.is_valid():
                pedido_form.save()
            return redirect('/prenda/crear_prenda/'+str(id_pedido))
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'pedido/crear_pedido.html',{'pedido_form':pedido_form,'detalles':detalles, 'error':error,'id_pedido':id_pedido})

#Editar un pedido
def EditarPedido (request,id_pedido):
    try:
        error = None
        pedido_form=None
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        if request.method=='GET':
            pedido_form=PedidoForm(instance=pedido)
        else:
            pedido_form=PedidoForm(request.POST, instance=pedido)
            if pedido_form.is_valid():
                pedido_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'pedido/crear_pedido.html',{'pedido_form':pedido_form, 'error':error})
#Eliminar un pedido
def EliminarPedido (request,id_pedido):
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    if request.method=='POST':
        pedido.delete()
        return redirect('pedido:listar_pedido')
    return render(request,'pedido/eliminar_pedido.html',{'pedido':pedido})
