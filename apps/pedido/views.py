from django.shortcuts import render, redirect
from tp_final.forms import PedidoForm, DetalleForm
from .models import Pedido, Detalle
from django.core.exceptions import ObjectDoesNotExist

#Crear un pedido
def CrearPedido (request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido_form.save()
            return ListarPedido(request)
    else:
        pedido_form = PedidoForm()
    return render(request, 'pedido/crear_pedido.html',{'pedido_form':pedido_form})
#Listar todos los pedidoes
def ListarPedido (request):
    pedidos = Pedido.objects.all()
    return render(request,'pedido/listar_pedido.html',{'pedidos':pedidos})
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
