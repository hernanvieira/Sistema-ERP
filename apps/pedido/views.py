from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import PedidoForm, DetalleForm, PrendaForm, IngredienteForm, DetalleForm,Detalle_envioForm, ClienteForm, Estado_pedidoForm
from .models import Pedido, Detalle, Entregas, Faltante, Detalle_envio
from apps.prenda.models import Prenda, Tipo_prenda, Ingrediente
from apps.estado.models import Estado_pedido, Estado
from apps.prenda.views import CrearPrenda
from apps.material.models import Material
from apps.cliente.models import Cliente
from django.core.exceptions import ObjectDoesNotExist
from tp_final import urls
import datetime

from datetime import datetime, timedelta, date

from django.contrib import messages
from config.models import Configuracion, ConfiguracionMensaje
from django.core.mail import EmailMessage
from django.db.models import Sum

from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .Serializers import *

import json
from django.http import HttpResponse
from django.http import JsonResponse



def NuevoPedido (request):
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
        if 'boton_crear_cliente' in request.POST:
            cliente_form = ClienteForm(request.POST)
            if cliente_form.is_valid():
                cliente_form.save()
                messages.success(request, 'Se agregó correctamente el cliente')
            else:
                messages.error(request, 'Error al crear el cliente')
        if 'boton_agregar' in request.POST:
            pedido_form = PedidoForm(request.POST)
            prenda_form = PrendaForm(request.POST) # lupy estubo aki peligro borre este mensaje para su comodidad
            if pedido_form.is_valid():
                pedido = pedido_form.save()
                id_pedido = pedido.id_pedido
                return redirect('/prenda/crear_prenda/'+str(id_pedido))
            else:
                messages.error(request, 'No se puede introducir valores negativos')
    else:
        pedido_form = PedidoForm()
        cliente_form = ClienteForm()
    pedido_form = PedidoForm()
    return render(request, 'pedido/nuevo_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'pedido_form':pedido_form, 'cliente_form':cliente_form})

def ConfirmarEntrega (request,id_pedido,id_cliente):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    form = Detalle_envioForm()
    pedido = Pedido.objects.get(id_pedido = id_pedido)
    cliente = Cliente.objects.get(dni = id_cliente)
    try:
        if request.method == 'POST':
            lista = request.POST.getlist('dia')
            domicilio = request.POST.get('domicilio')
            desde = request.POST.get('desde')
            hasta = request.POST.get('hasta')
            dia = request.POST.get('dia')
            if desde != '' and hasta != '' :
                envio_datos = Detalle_envio.objects.filter(pedido=pedido, cliente=cliente)
                if envio_datos:
                    for envio in envio_datos:
                        envio.delete()
                for dia in lista:
                    Detalle_envio.objects.create(domicilio = domicilio, desde = desde, hasta = hasta, dia = dia, cliente = cliente, pedido = pedido)
                messages.success(request,'Gracias')
            else:
                messages.error(request, 'Introduzcas horarios disponibles')
                form = Detalle_envioForm(request.POST)
                return render(request, 'pedido/confirmar_entrega.html',{'form':form})
    except Exception as e:
        messages.error(request, 'Ocurrió un error al enviar los datos')
        form = Detalle_envioForm(request.POST)
        return render(request, 'pedido/confirmar_entrega.html',{'form':form})
    else:
        form = Detalle_envioForm()
    return render(request, 'pedido/confirmar_entrega.html',{'form':form})

#Crear un pedido
def CrearPedido (request):
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
        if 'boton_crear_cliente' in request.POST:
            cliente_form = ClienteForm(request.POST)
            if cliente_form.is_valid():
                cliente_form.save()
                messages.success(request, 'Se agregó correctamente el cliente')
            else:
                messages.error(request, 'Error al crear el cliente')
        if 'boton_agregar' in request.POST:
            pedido_form = PedidoForm(request.POST)
            prenda_form = PrendaForm(request.POST) # lupy estubo aki peligro borre este mensaje para su comodidad
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
            id_pedido = pedido.id_pedido
            print(id_pedido)
            if pedido.seña != None:
                pedido.save()
                return redirect('pedido/listar_pedido/'+str(id_pedido))

            else:
                cliente_form = ClienteForm(request.POST)
                messages.error(request, 'Debe agregar prendas')
    else:
        pedido_form = PedidoForm()
        cliente_form = ClienteForm()
    pedido_form = PedidoForm()
    return render(request, 'pedido/crear_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'pedido_form':pedido_form, 'cliente_form':cliente_form})

#Listar todos los pedidos
def ListarPedido (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedidos = Pedido.objects.all().exclude(confirmado=False)
    reporte = Configuracion.objects.all().last()
    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux
    return render(request,'pedido/listar_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'reporte':reporte,'pedidos':pedidos})

def ListarPedido2 (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedidos = Pedido.objects.all().exclude(confirmado=False)
    reporte = Configuracion.objects.all().last()
    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux
    return render(request,'pedido/listar_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'id_pedido':id_pedido,'reporte':reporte,'pedidos':pedidos})

#Volver al pedido
def VolverPedido (request,id_pedido):
        #Notificaciones
        pedidos = Pedido.objects.all().exclude(confirmado=False)
        envios_noti = []
        for pedido in pedidos:
            envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
            if envio_temp:
                envios_noti.append(envio_temp)
        envios_not = envios_noti[:3]
        envio_count = len(envios_noti)

        detalles = None
        pedido_form=None
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        pedido_id = pedido.id_pedido
        detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
        mensaje = ConfiguracionMensaje.objects.all().last()
        reporte = Configuracion.objects.all().last()

        if request.method=='GET':
            if not detalles:
                pedido.delete()
                return redirect('/pedido/nuevo_pedido')
            pedido_form=PedidoForm(instance=pedido)
        else:
            if 'boton_agregar' in request.POST:
                pedido_form=PedidoForm(request.POST, instance=pedido)
                if pedido_form.is_valid():
                    pedido_form.save()
                return redirect('/prenda/crear_prenda/'+str(id_pedido))

            if 'boton_cancelar' in request.POST:
                detalles = Detalle.objects.filter(pedido = pedido)
                for detalle in detalles:
                    detalle.delete()
                    detalle.prenda.delete()
                pedido.delete()
                return redirect('/pedido/nuevo_pedido')

            if 'boton_finalizar' in request.POST:
                pedido_form = PedidoForm(request.POST, instance=pedido)
                pedido = pedido_form.save(commit=False)

                estado_enespera = Estado.objects.get(id_estado = 6)

                estado_pedido = Estado_pedido.objects.create(fecha=date.today(), estado = estado_enespera, pedido = pedido)

                pedido.confirmado = True

                from django.template.loader import render_to_string
                from django.core.mail import EmailMultiAlternatives
                #
                text_content = 'Detalle de pedido'
                msg_html = render_to_string('recibo.html', {'pedido':pedido, 'reporte':reporte, 'detalles':detalles})
                html_content = msg_html
                msg = EmailMultiAlternatives('PROYECTO SOFTWARE', text_content, to=[pedido.cliente.correo])
                msg.attach_alternative(html_content, "text/html")
                try:
                    msg.send()
                except Exception as e:
                    print(e)
                id_pedido = pedido.id_pedido

                if pedido.seña != None:
                    pedido.save()
                    estado_pedido.save()
                    messages.success(request, 'Todo ocurrió correctamente')
                    return redirect('/pedido/listar_pedido/'+str(id_pedido))

                else:
                    cliente_form = ClienteForm(request.POST)
                    messages.error(request, 'Debe agregar prendas')
        cliente_form = ClienteForm(request.POST)

        return render(request,'pedido/crear_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'pedido':pedido,'pedido_form':pedido_form,'detalles':detalles,'cliente_form':cliente_form})

#Editar un pedido
def EditarPedido (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

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
    return render(request,'pedido/editar_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'pedido_form':pedido_form,'detalles':detalles})

#Editar un pedido
def VerPedido (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedido_form=None
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    mensaje = ConfiguracionMensaje.objects.all().last()
    cliente = pedido.cliente
    detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
    estados = Estado_pedido.objects.filter(pedido_id=id_pedido)
    entregas = Entregas.objects.filter(pedido=pedido)

    envio = Detalle_envio.objects.filter(pedido=pedido,cliente=pedido.cliente).first()
    envios = Detalle_envio.objects.filter(pedido=pedido,cliente=pedido.cliente)
    envio_dias = Detalle_envio.objects.filter(pedido=pedido,cliente=pedido.cliente).values_list('dia', flat=True)
    if envio:
        for envio in envios:
            envio.visto = True
            envio.save()

    ingredientes = Ingrediente.objects.values_list('prenda', flat=True)
    for ingrediente in ingredientes:
        print(ingrediente)
    if Estado_pedido.objects.filter(pedido_id=id_pedido).exists():
        estado = Estado_pedido.objects.filter(pedido_id=id_pedido).order_by('-id_estado_pedido')[0]
    else:
        estado = None
    if request.method=='GET':
        pedido_form=PedidoForm(instance=pedido)
        envios_noti = []
        for pedido in pedidos:
            envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
            if envio_temp:
                envios_noti.append(envio_temp)
        envios_not = envios_noti[:3]
        envio_count = len(envios_noti)
    else:
        if 'boton_cancelar' in request.POST:
            CancelarPedido(request,id_pedido)
            redireccionar = 0
            prendas = Detalle.objects.filter(pedido = pedido)
            for detalle in prendas:
                prenda = detalle.prenda
                ingredientes = Ingrediente.objects.filter(prenda = prenda).exists()
                if ingredientes:
                    redireccionar=1
            if redireccionar == 1:
                return redirect('/pedido/materiales_utilizados/'+str(id_pedido))
        if 'boton_entregar' in request.POST:
            EntregarPedido(request,id_pedido)
        if 'boton_registrar_entega' in request.POST:
            peticion = request.POST.copy() # Obtengo una copia del request
            usuario = request.user #Obtengo el usuario registrado actualmente
            peticion_valor = peticion.pop('registrar_entrega')[0] #Obtengo el valor de la enterga
            pedido.entrega += int(peticion_valor) #Sumo la entrega al pedido

            saldo = pedido.precio_total - pedido.entrega #Obtengo el saldo despues de registrar la entrega

            saldoaux = saldo
            if saldo < 0:
                saldoaux = 0
            entrega = Entregas.objects.create(monto = peticion_valor, pedido = pedido, saldo = saldoaux, usuario = usuario) #Creamos la entrega
            entrega.save()

            if saldo == 0:
                pedido.save()
                messages.success(request, 'Se registró la entrega y se completó el pago')

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: $0,00' , to=[pedido.cliente.correo])
                try:
                    email.send()
                except Exception as e:
                    print(e)


            if saldo > 0:
                pedido.save()
                messages.success(request, 'Se registró la entrega, resta un saldo de: ' + str(saldo))

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: ' + str(saldo), to=[pedido.cliente.correo])
                try:
                    email.send()
                except Exception as e:
                    print(e)

            if saldo < 0:
                pedido.entrega = pedido.precio_total
                pedido.save()
                messages.success(request, 'Se registró la entrega y se completó el pago. El cambio es de: ' + str(abs(saldo)))

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: $0,00' , to=[pedido.cliente.correo])
                try:
                    email.send()
                except Exception as e:
                    print(e)

            if pedido.entrega >= pedido.seña:
                estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
                estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
                estado_en_produccion = Estado.objects.get(id_estado = 2) #Obtengo el estado "En produccion"

                estado = Estado_pedido.objects.filter(pedido_id=id_pedido).order_by('-id_estado_pedido')[0]

                if estado.estado != estado_en_produccion: #Si no estaba en produccion

                    estado_pedido.estado = estado_en_produccion #Asocio el estado "En produccion"
                    estado_pedido.pedido = pedido # Asocio el pedido actual
                    estado_pedido.fecha = date.today() #Establezco como fecha el dia de hoy

                    estado_pedido.save()#Guardo el estado

                    email = EmailMessage('PROYECTO SOFTWARE', mensaje.en_produccion, to=[pedido.cliente.correo])
                    try:
                        email.send()
                    except Exception as e:
                        print(e)

        pedido_form=PedidoForm(instance=pedido)
        if Estado_pedido.objects.filter(pedido_id=id_pedido).exists():
            estado = Estado_pedido.objects.filter(pedido=pedido).order_by('-id_estado_pedido')[0]
        else:
            estado = None
    return render(request,'pedido/ver_pedido.html',{'envio_count':envio_count,'envios_noti':envios_noti,'envio':envio,'envio_dias':envio_dias,'ingredientes':ingredientes,'cliente':cliente,'pedido_form':pedido_form,'detalles':detalles, 'estado':estado,'pedido':pedido,'estados':estados,'entregas':entregas})


#Eliminar un pedido
def EliminarPedido (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

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
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido) #obtengo el pedido
    pedido.cancelado = True #Cambio el estado de cancelado a True
    estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario
    estado_pedido = estado_pedido_form.save(commit = False) #Commit False de pedido con los valores recibidos
    mensaje = ConfiguracionMensaje.objects.all().last() #Obtengo las ultimas configuraciones para enviar correo

    estado_cancelado = Estado.objects.get(id_estado = 5) #Obtengo el estado cancelado

    estado_pedido.estado = estado_cancelado #Establezco el estado cancelado al estado del pedido
    estado_pedido.pedido = pedido #Asocio el pedido al estado
    estado_pedido.fecha = date.today() #Establezco la fecha actual al estado

    pedido.save() #Actualizo el pedido
    estado_pedido.save() #Guardo el estado
    messages.warning(request, 'Se canceló el pedido') #Informo que el pedido se canceló

    # Envio de correo
    email = EmailMessage('PROYECTO SOFTWARE', mensaje.cancelado, to=[pedido.cliente.correo])
    try:
        email.send()
    except Exception as e:
        print(e)

    # Reputación
    cliente = pedido.cliente # Obtengo el cliente

    reputacion = cliente.reputacion #Obtengo la reputación

    check = str(request.POST['optradio'])
    if check =='checkMM':
        reputacion -= 40
    if check=='checkM':
        reputacion -= 20
    if check=='checkR':
        reputacion += 5
    if check=='checkB':
        reputacion += 10
    if check=='checkMB':
        reputacion += 20
    cliente.reputacion = reputacion #Asocio el valor de reputación actualizado
    cliente.save() #Actualizo el cliente

    #Actualización de stock
    detalles = Detalle.objects.filter(pedido = pedido) #Obtengo las prendas
    ingredientes_list = [] #Creo lista para obtener los ingredientes de todas las prendas
    for detalle in detalles: #Por cada detalle (prenda)
        ingredientes = Ingrediente.objects.filter(prenda = detalle.prenda) #Obtengo los ingredientes de la prenda actual
        for ingrediente in ingredientes: #Por cada ingrediente
            ingredientes_list.append(ingrediente) #Agrego el ingrediente a la lista

    for ingrediente in ingrediente_list:
        ingrediente.material.stock += ingrediente.cantidadxdetalle
        ingrediente.material.save()
        if ingrediente.disponibilidad == "FALTANTE":
            faltante = Faltante.objects.get(prenda = ingrediente.prenda, material = ingrediente.material)
            if faltante:
                faltante.delete()
        else:
            #Solventar Faltantes
            faltantes = Faltante.objects.filter(material = material)
            if faltantes:
                ingredientes_faltante = Ingrediente.objects.filter(material = material, disponibilidad = "FALTANTE")
                for ingrediente in ingredientes_faltante:

                    faltante = Faltante.objects.get(material = material, prenda = ingrediente.prenda)

                    if cantidad != 0: #Si la cantidad es distinta de 0
                        if cantidad < faltante.faltante: #Si la cantidad es menor al faltante a solventar
                            faltante.faltante -= cantidad #Resto al faltante la cantidad introducida
                            cantidad = 0 #Establesco la cantidad en 0 porque la ocupé por completo
                            faltante.save() #actualizo el faltante
                        if cantidad >= faltante.faltante: #Si la cantidad es mayor o igual al faltante
                            cantidad -= faltante.faltante #Resto a la cantidad lo que voy a utilizar para solventar el faltante
                            faltante.delete() #Elimino el faltante al solventarlo por completo

                            #Calcular disponibilidad
                            if ingrediente.cantidadxdetalle > ingrediente.material.stock_minimo:#Si el ingrediente es mayor al stock minimo del material actualizado
                                ingrediente.disponibilidad = "DISPONIBLE" #Establezco la disponibilidad
                            else: #Si el ingrediente es menor o igual al stock minimo
                                ingrediente.disponibilidad = "STOCK MÍNIMO" #Establezco la disponibilidad
                            ingrediente.save() #Actualizo el ingrediente



def MaterialesUtilizados(request, id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedido = Pedido.objects.get(id_pedido= id_pedido) #
    if request.method=='POST':
        peticion = request.POST.copy() # OBtengo una copia del request
        peticion_sobrante = peticion.pop('input_sobrante') # Obtengo el valor de los sobrantes
        peticion_id_ingrediente = peticion.pop('input_id_ingrediente') # Obtengo los id de los materiales
        i=0 #Inicializo i en 0
        for id_ingrediente in peticion_id_ingrediente: #Por cada ingrediente recibido
            ingrediente = Ingrediente.objects.get(id_ingrediente= id_ingrediente) #Obtengo el ingrediente
            sobrante = peticion_sobrante[i] #Obtengo el sobrante
            i+=1 #Incremento i en 1
            if ingrediente.disponibilidad == "DISPONIBLE" or ingrediente.disponibilidad == "STOCK MÍNIMO": #Si esta disponible el stock del ingrediente
                ingrediente.material.stock += int(sobrante) #Sumo el material sobrante al stock del material
                ingrediente.material.save() #Actualizo el material
            if ingrediente.disponibilidad == "FALTANTE": #Si tiene faltante
                ingrediente.material.stock += int(sobrante) #Sumo el sobrante que recibo
                ingrediente.material.save() #Actualizo el stock

                prenda = ingrediente.prenda #Obtengo la prenda del ingrediente
                material = ingrediente.material #Obtengo el material del ingrediente
                faltante = Faltante.objects.get(prenda = prenda, material = material) #Obtengo el faltante
                faltante.delete() #Elimino el faltante

    else:
        prendas = Detalle.objects.filter(pedido = pedido)
        a=[]
        for detalle in prendas:
            prenda = detalle.prenda
            ingredientes = Ingrediente.objects.filter(prenda = prenda)
            for ingrediente in ingredientes:
                a.append(ingrediente)
        ingredientes = a
        return render(request,'pedido/materiales_utilizados.html',{'envios_not':envios_not,'envio_count':envio_count,'pedido':pedido,'ingredientes':ingredientes,'prendas':prendas})
    return redirect('/pedido/ver_pedido/' + str(id_pedido))


#Finalizar un pedido
def FinalizarPedido (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
    estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
    estado_finalizado = Estado.objects.get(id_estado = 3) #Obtengo el estado "Finalizar"
    mensaje = ConfiguracionMensaje.objects.all().last()


    estado_pedido.estado = estado_finalizado #Asocio el estado "En produccion"
    estado_pedido.pedido = pedido # Asocio el pedido actual
    estado_pedido.fecha = date.today() #Establezco como fecha el dia de hoy

    estado_pedido.save()#Guardo el estado
    pedido.save()
    estado_pedido.save()

    email = EmailMessage('PROYECTO SOFTWARE', mensaje.finalizado + 'http://localhost:8000/pedido/confirmar_entrega/'+str(pedido.pk)+'/'+str(pedido.cliente.pk), to=[pedido.cliente.correo])
    try:
        email.send()
    except Exception as e:
        print(e)

    return redirect('/pedido/ver_pedido/' + str(id_pedido))

#Entregar un pedido
def EntregarPedido (request,id_pedido):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
    estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
    estado_entregado = Estado.objects.get(id_estado = 4) #Obtengo el estado "Finalizar"
    mensaje = ConfiguracionMensaje.objects.all().last()

    estado_pedido.estado = estado_entregado #Asocio el estado "En produccion"
    estado_pedido.pedido = pedido # Asocio el pedido actual
    estado_pedido.fecha = date.today() #Establezco como fecha el dia de hoy

    estado_pedido.save()#Guardo el estado
    pedido.save()
    estado_pedido.save()
    messages.success(request, 'Se entregó el pedido')

    email = EmailMessage('PROYECTO SOFTWARE', mensaje.entregado, to=[pedido.cliente.correo])
    try:
        email.send()
    except Exception as e:
        print(e)

    # Reputación
    cliente = pedido.cliente # Obtengo el cliente

    reputacion = cliente.reputacion

    check = str(request.POST['optradio'])
    print(check)
    if check =='checkMM':
        reputacion -= 40
    if check=='checkM':
        reputacion -= 20
    if check=='checkR':
        reputacion += 5
    if check=='checkB':
        reputacion += 10
    if check=='checkMB':
        reputacion += 20
    cliente.reputacion = reputacion
    cliente.save()

    return redirect('/pedido/ver_pedido/' + str(id_pedido))


#Pagina de auditoria
def Auditoria(request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    reporte = Configuracion.objects.all().last()
    auditoria =  Pedido.history.all()
    return render(request, 'auditoria_pedido.html',{'envios_not':envios_not,'envio_count':envio_count,'auditoria':auditoria,'reporte':reporte})

def ListaCompras (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    reporte = Configuracion.objects.all().last()
    print(reporte)
    if request.method=='GET':
        lista = Faltante.objects.values('material').order_by('material').annotate(sum=Sum('faltante')) #Obtengo un queryset con la suma de faltante agrupado por cada material, solo me trae el id
        lista2 = Faltante.objects.all()
        #Creo una lista para guardar los objetos de cada material
        materiales=[]
        #Obtengo los objetos y los agrego a la lista
        for i in range(len(lista)):
            material = Material.objects.get(id_material = lista[i]['material'])
            materiales.append(material)

        #Intercambio los id de cada material por el objeto en si
        for i in range(len(materiales)):
            lista[i]['material'] = materiales[i]

        return render(request,'prenda/lista_compras.html',{'envios_not':envios_not,'envio_count':envio_count,'reporte':reporte,'lista':lista, 'lista2':lista2})

def Notificaciones(request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    if request.method == 'GET':
        return render(request,'pedido/notificaciones.html',{'envios_not':envios_not,'envio_count':envio_count,'envios_noti':envios_noti})

#Ver Cambios
def VerAuditoria(request,pk,id_history):
    historial = Pedido.history.filter(id_pedido=pk)
    for i in range(len(historial)):
        if historial[i].pk == id_history:
            audit_regsolo = historial[i]
            delta = audit_regsolo.diff_against(historial[i+1])
            data = []
            for change in delta.changes:
                dic = {'change':change.field,'old':change.old, 'new':change.new}
                data.append(dic)
            break
    return JsonResponse(data,safe=False)

#Notificaciones
# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def _init_(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self)._init_(content, **kwargs)
#
#
# @csrf_exempt
# def Notificaciones(request):
#     print("TAENTRa")
#     pedidos = Pedido.objects.all().exclude(confirmado=False)
#     envios_noti = []
#     for pedido in pedidos:
#         envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
#         if envio_temp:
#             envios_noti.append(envio_temp)
#     envio_count = len(envios_noti)
#
#     serializer=Detalle_envioSerializer(envios_noti,many=True)
#     result=dict()
#     result = serializer.data
#
#     import json
#     output_dict = json.loads(json.dumps(serializer.data))
#
#     print(type(output_dict))
#
#     return JSONResponse(output_dict[0]['pedido'].values())
