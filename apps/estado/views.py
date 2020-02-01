from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import EstadoForm, Tipo_prendaForm, PrendaForm, IngredienteForm, DetalleForm
from .models import Estado, Estado_pedido, Estado_lote
from django.contrib import messages

from apps.pedido.models import Pedido, Detalle_envio

#Crear un Estado
def CrearEstado (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estados = Estado.objects.all()
    if request.method == 'POST':
        estado_form = EstadoForm(request.POST)
        print(estado_form.errors)
        if estado_form.is_valid():
            estado = estado_form.save()
            return ListarEstado(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de crear el estado')
    else:
        estado_form = EstadoForm()
    return render(request, 'estado/crear_estado.html',{'envios_not':envios_not,'envio_count':envio_count,'estados':estados,'estado_form':estado_form})

#Listar todos los estados
def ListarEstado (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estados = Estado.objects.all()
    return render(request,'estado/listar_estado.html',{'envios_not':envios_not,'envio_count':envio_count,'estados':estados})

#Editar un estado
def EditarEstado (request,id_estado):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estados = Estado.objects.all()
    estado_form=None
    estado = Estado.objects.get(id_estado=id_estado)
    if request.method=='GET':
        estado_form=EstadoForm(instance=estado)
    else:
        estado_form=EstadoForm(request.POST, instance=estado)
        if estado_form.is_valid():
            estado_form.save()
        return render(request, 'estado/crear_estado.html',{'envios_not':envios_not,'envio_count':envio_count,'estados':estados,'estado_form':estado_form})
    return render(request,'estado/editar_estado.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_form':estado_form})

#Eliminar un estado
def EliminarEstado (request,id_estado):
    estado = get_object_or_404(Estado, id_estado=id_estado)
    try:
        estado.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el estado')
    return ListarEstado(request)

#Crear un Estado_pedido
def CrearEstado_pedido (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    if request.method == 'POST':
        estado_pedido_form = Estado_pedidoForm(request.POST)
        if estado_pedido_form.is_valid():
            estado_pedido = estado_pedido_form.save()
            return ListarEstado_pedido(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de crear el estado_pedido')
    else:
        estado_pedido_form = Estado_pedidoForm()
    return render(request, 'estado_pedido/crear_estado_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_pedido_form':estado_pedido_form})

#Listar todos los estado_pedidos
def ListarEstado_pedido (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_pedidos = Estado_pedido.objects.all()
    return render(request,'estado_pedido/listar_estado_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_pedidos':estado_pedidos})

#Editar un estado_pedido
def EditarEstado_pedido (request,id_estado_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_pedido_form=None
    estado_pedido = Estado_pedido.objects.get(id_estado_pedido=id_estado_pedido)
    if request.method=='GET':
        estado_pedido_form=Estado_pedidoForm(instance=estado_pedido)
    else:
        estado_pedido_form=estado_pedidoForm(request.POST, instance=estado_pedido)
        if estado_pedido_form.is_valid():
            estado_pedido_form.save()
        return redirect('index')
    return render(request,'prenda/crear_estado.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_pedido_form':estado_pedido_form})

#Eliminar un estado_pedido
def EliminarEstado_pedido (request,id_estado_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_pedido = get_object_or_404(estado_pedido, id_estado_pedido=id_estado_pedido)
    if request.method=='POST':
        estado_pedido.delete()
        return redirect('prenda:listar_estado_pedido')
    return render(request,'prenda/eliminar_estado_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_pedido':estado_pedido})

#Crear un Estado_lote
def CrearEstado_lote (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    if request.method == 'POST':
        estado_lote_form = Estado_loteForm(request.POST)
        if estado_lote_form.is_valid():
            estado_lote = estado_lote_form.save()
            return ListarEstado_lote(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de crear el estado_lote')
    else:
        estado_lote_form = Estado_loteForm()
    return render(request, 'estado_lote/crear_estado_lote.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_lote_form':estado_lote_form})

#Listar todos los estado_lotes
def ListarEstado_lote (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_lotes = Estado_lote.objects.all()
    return render(request,'estado_lote/listar_estado_lote.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_lotes':estado_lotes})

#Editar un estado_lote
def EditarEstado_lote (request,id_estado_lote):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_lote_form=None
    estado_lote = Estado_lote.objects.get(id_estado_lote=id_estado_lote)
    if request.method=='GET':
        estado_lote_form=Estado_loteForm(instance=estado_lote)
    else:
        estado_lote_form=estado_loteForm(request.POST, instance=estado_lote)
        if estado_lote_form.is_valid():
            estado_lote_form.save()
        return redirect('index')
    return render(request,'prenda/crear_estado_lote.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_lote_form':estado_lote_form})

#Eliminar un estado_lote
def EliminarEstado_lote(request,id_estado_lote):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    estado_lote = get_object_or_404(estado_lote, id_estado_lote=id_estado_lote)
    if request.method=='POST':
        estado_lote.delete()
        return redirect('prenda:listar_estado_lote')
    return render(request,'prenda/eliminar_estado_lote.html',{'envios_not':envios_not,'envio_count':envio_count,'estado_lote':estado_lote})
