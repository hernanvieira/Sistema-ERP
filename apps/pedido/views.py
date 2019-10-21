from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import PedidoForm, DetalleForm, PrendaForm, IngredienteForm, DetalleForm, ClienteForm
from .models import Pedido, Detalle
from apps.prenda.models import Prenda
from apps.prenda.views import CrearPrenda
from django.core.exceptions import ObjectDoesNotExist
from tp_final import urls
import datetime
from django.contrib import messages
#Crear un pedido
def CrearPedido (request):
    if request.method == 'POST':
        if 'boton_crear_cliente' in request.POST:
            cliente_form = ClienteForm(request.POST)
            if cliente_form.is_valid():
                cliente_form.save()
                messages.success(request, 'Se agregó correctamente el cliente')
            else:
                messages.error(request, 'Error al crear el cliente')
        if 'boton_agregar' in request.POST:
            pedido_form = PedidoForm(request.POST)
            prenda_form = PrendaForm(request.POST)
            if pedido_form.is_valid():
                pedido = pedido_form.save(commit = False)
                if pedido.fecha_entrega != None:
                    fecha = datetime.datetime.strptime(str(pedido.fecha_entrega), '%Y-%m-%d')
                    if fecha.date() > datetime.date.today():
                        pedido = pedido_form.save()
                        id_pedido = pedido.id_pedido
                        return redirect('/prenda/crear_prenda/'+str(id_pedido))
                    else:
                        messages.error(request, 'La fecha debe ser posterior a la actual')
                else:
                    pedido = pedido_form.save()
                    id_pedido = pedido.id_pedido
                    return redirect('/prenda/crear_prenda/'+str(id_pedido))
            else:
                messages.error(request, 'No se puede introducir valores negativos')
        if 'boton_finalizar' in request.POST:
            pedido_form = PedidoForm(request.POST)
            pedido = pedido_form.save()
            if pedido.precio_total != None:
                pedido.save()
                return redirect('/pedido/listar_pedido/')
            else:
                cliente_form = ClienteForm(request.POST)
                messages.error(request, 'Debe agregar prendas')
    else:
        pedido_form = PedidoForm()
        cliente_form = ClienteForm()
    pedido_form = PedidoForm()
    return render(request, 'pedido/crear_pedido.html',{'pedido_form':pedido_form, 'cliente_form':cliente_form})

#Listar todos los pedidos
def ListarPedido (request):
    pedidos = Pedido.objects.all()
    return render(request,'pedido/listar_pedido.html',{'pedidos':pedidos})

#Volver al pedido
def VolverPedido (request,id_pedido):
        detalles = None
        pedido_form=None
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        pedido_id = pedido.id_pedido
        detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
        if request.method=='GET':
            pedido_form=PedidoForm(instance=pedido)
        else:
            if 'boton_agregar' in request.POST:
                pedido_form=PedidoForm(request.POST, instance=pedido)
                if pedido_form.is_valid():
                    pedido_form.save()
                return redirect('/prenda/crear_prenda/'+str(id_pedido))
            if 'boton_finalizar' in request.POST:
                pedido_form = PedidoForm(request.POST, instance=pedido)
                pedido = pedido_form.save(commit=False)
                if pedido.precio_total != None:
                    pedido.save()
                    messages.success(request, 'Todo ocurrió correctamente')
                    return redirect('/pedido/listar_pedido/')
                else:
                    cliente_form = ClienteForm(request.POST)
                    messages.error(request, 'Debe agregar prendas')
        cliente_form = ClienteForm(request.POST)
        return render(request,'pedido/crear_pedido.html',{'pedido_form':pedido_form,'detalles':detalles,'cliente_form':cliente_form})

#Editar un pedido
def EditarPedido (request,id_pedido):
    pedido_form=None
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedidos = Pedido.objects.all()
    detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
    if request.method=='GET':
        pedido_form=PedidoForm(instance=pedido)
    else:
        if 'boton_agregar' in request.POST:
            pedido_form=PedidoForm(request.POST, instance=pedido)
            if pedido_form.is_valid():
                pedido_form.save()
            return redirect('/prenda/crear_prenda/'+str(id_pedido))
        if 'boton_finalizar' in request.POST:
            pedido_form = PedidoForm(request.POST, instance=pedido)
            pedido = pedido_form.save(commit=False)
            if pedido.precio_total != None:
                pedido.save()
                return redirect('/pedido/listar_pedido/')
            else:
                cliente_form = ClienteForm(request.POST)
                messages.error(request, 'Debe agregar prendas')
    return render(request,'pedido/editar_pedido.html',{'pedido_form':pedido_form,'detalles':detalles})
#Eliminar un pedido
def EliminarPedido (request,id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    try:
        pedido.delete()
        messages.warning(request, 'Se eliminó el pedido')
    except Exception as e:
        messages.error(request, "Ocurrió un error al tratar de eliminar el pedido " + str(id_pedido))
    pedidos = Pedido.objects.all()
    return ListarPedido(request)
