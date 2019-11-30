from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import PedidoForm, DetalleForm, PrendaForm, IngredienteForm, DetalleForm, ClienteForm, Estado_pedidoForm
from .models import Pedido, Detalle
from apps.prenda.models import Prenda, Tipo_prenda
from apps.estado.models import Estado_pedido, Estado
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
            pedido = pedido_form.save(commit=False)

            if pedido.seña != None:
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
    aux = []
    for p in pedidos:
        a = Estado_pedido.objects.filter(pedido = p).last()
        if a != None:
            aux.append(a)
    pedidos = aux
    print("HOLASI")
    print(pedidos)
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

                estado_pedido_form = Estado_pedidoForm()
                estado_pedido = estado_pedido_form.save(commit = False)

                estado_enespera = Estado.objects.get(id_estado = 6)

                estado_pedido.estado = estado_enespera
                estado_pedido.pedido = pedido
                estado_pedido.fecha = datetime.date.today()

                if pedido.seña != None:
                    pedido.save()
                    estado_pedido.save()
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

#Editar un pedido
def VerPedido (request,id_pedido):
    pedido_form=None
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedidos = Pedido.objects.all()
    cliente = pedido.cliente
    detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
    if Estado_pedido.objects.filter(pedido_id=id_pedido). exists():
        estado = Estado_pedido.objects.filter(pedido_id=id_pedido).latest()
    else:
        estado = None
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
    return render(request,'pedido/ver_pedido.html',{'cliente':cliente,'pedido_form':pedido_form,'detalles':detalles, 'estado':estado,'pedido':pedido})


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

#Cancelar un pedido
def CancelarPedido (request,id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedido.cancelado = True
    estado_pedido_form = Estado_pedidoForm()
    estado_pedido = estado_pedido_form.save(commit = False)

    estado_cancelado = Estado.objects.get(id_estado = 5)

    estado_pedido.estado = estado_cancelado
    estado_pedido.pedido = pedido
    estado_pedido.fecha = datetime.date.today()

    pedido.save()
    estado_pedido.save()
    messages.warning(request, 'Se canceló el pedido')
    # except Exception as e:
    #     messages.error(request, "Ocurrió un error al tratar de cancelar el pedido " + str(id_pedido))
    pedidos = Pedido.objects.all()
    return ListarPedido(request)


#Pagina de auditoria
def Auditoria(request):
    auditoria =  Pedido.history.all()
    return render(request, 'auditoria_pedido.html',{'auditoria':auditoria})
