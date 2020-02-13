from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import ClienteForm
from .models import Cliente
from django.core.exceptions import *
from django.contrib import messages
from config.models import Configuracion
from apps.pedido.models import Faltante, Detalle_envio, Pedido, Detalle
from apps.material.models import Material
from apps.pedido.views import FinalizarPedido

from config.models import Configuracion, ConfiguracionMensaje
from django.core.mail import EmailMessage

from django.db.models import Sum

import poplib # Recibir correos

from apps.prenda.models import Tipo_prenda, Prenda
from apps.estado.models import Estado_pedido

from datetime import datetime, timedelta, date

from dateutil.relativedelta import relativedelta
import dateutil.parser

from django.db.models import Count

from django.http import JsonResponse

# Create your views here.

#Pagina de inicio
def Home(request):

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

    if request.method == 'POST':
        if 'button-actualizar' in request.POST:
            for pedido in pedidos:
                if pedido.fecha_entrega <= date.today():
                    FinalizarPedido(request,pedido.pk)
            pedidos_finalizados = Pedido.objects.filter(estado_pedido__estado_id = 3).exclude(detalle_envio__isnull = False).exclude(estado_pedido__estado_id = 4)
            for pedido in pedidos_finalizados:
                diferencia = 0
                estado = Estado_pedido.objects.filter(pedido = pedido).order_by('-id_estado_pedido')[0]

                fecha = estado.fecha
                fecha = fecha.strftime('%d/%m/%Y')
                fecha = datetime.strptime(fecha,'%d/%m/%Y')
                hoy = datetime.now()      # Tipo: datetime.datetime
                #hoy = dateutil.parser.parse(hoy)
                hoy = hoy.strftime('%d/%m/%Y')
                hoy = datetime.strptime(hoy, '%d/%m/%Y')
                diferencia = hoy - fecha  # Tipo resultante: datetime.timedelta
                diferencia = diferencia.days
                if diferencia > 5:
                    mensaje = ConfiguracionMensaje.objects.all().last()
                    email = EmailMessage('PROYECTO SOFTWARE', mensaje.finalizado + 'http://localhost:8000/pedido/confirmar_entrega/'+str(pedido.pk)+'/'+str(pedido.cliente.pk), to=[pedido.cliente.correo])
                    try:
                        email.send()
                    except Exception as e:
                        print(e)

            print(pedidos_finalizados)

    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux

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



    return render(request, 'index.html',{'envio_count':envio_count,'envios_not':envios_not,'reporte':reporte,'pedidos':pedidos, 'lista':lista})

#Pagina de estadisticas
def Estadistica(request):
    #Estadistica Bar
    # lista_bar = []
    # tipo_prendas_list = Tipo_prenda.objects.all()
    # for tipo_prenda in tipo_prendas_list:
    #     diccionario = {
    #     'tipo_prenda':tipo_prenda.nombre,
    #     'valor':Detalle.objects.filter(prenda__tipo_prenda = tipo_prenda).aggregate(Sum('cantidad'))['cantidad__sum']
    #
    #     }
    #     lista_bar.append(diccionario)

    #Estadistica Chart
    lista_chart = []
    tipo_prendas_list = Tipo_prenda.objects.all()
    for tipo_prenda in tipo_prendas_list:
        diccionario = {
        'prenda':tipo_prenda.nombre,
        'valor':Detalle.objects.filter(prenda__tipo_prenda = tipo_prenda).aggregate(Sum('cantidad'))['cantidad__sum']
        }
        lista_chart.append(diccionario)

    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    return render(request, 'estadistica.html',{'envios_not':envios_not,'envio_count':envio_count,'lista_chart':lista_chart})

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

    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    return render(request, 'cliente/crear_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'cliente_form':cliente_form})

#Editar un cliente
def VerCliente (request,dni):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)
    
    try:
        cliente_form=None
        cliente = Cliente.objects.get(dni=dni)
        pedidos = Pedido.objects.filter(cliente = cliente).exclude(confirmado = False)
        estados=[]
        for pedido in pedidos:
            estado = Estado_pedido.objects.filter(pedido=pedido).order_by('-id_estado_pedido')[0]

            print("ESTADUKI")
            print(estado)
            estados.append(estado)
        print(estados)
        if request.method=='GET':
            cliente_form=ClienteForm(instance=cliente)
        else:
            cliente_form=ClienteForm(request.POST, instance=cliente)
            if cliente_form.is_valid():
                cliente_form.save()
            return redirect('cliente:cliente_home')
    except ObjectDoesNotExist as e:
        error = e



    return render(request, 'cliente/ver_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'estados':estados,'pedidos':pedidos, 'cliente':cliente ,'cliente_form':cliente_form})

#Listar todos los clientes
def ListarCliente (request):
    clientes = Cliente.objects.all().exclude(activo = False)

    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    return render(request,'cliente/listar_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'clientes':clientes})
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

    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    return render(request, 'cliente/crear_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'cliente_form':cliente_form})

#Eliminar un cliente
def EliminarCliente (request,dni):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    cliente = get_object_or_404(Cliente,dni=dni)
    try:
        cliente.activo = False
        cliente.save()
        messages.warning(request, 'Se eliminó el cliente')
        clientes = Cliente.objects.all().exclude(activo = False)

        #pedidos de cliente en False
        pedidos = Pedido.objects.filter(cliente = cliente)
        for pedido in pedidos:
            pedido.confirmado = False
            pedido.save()

        return render(request,'cliente/index_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'cliente':cliente,'clientes':clientes})
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el cliente')
    clientes = Cliente.objects.all().exclude(activo = False)
    return render(request,'cliente/index_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'cliente':cliente,'clientes':clientes})

def ClienteHome(request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    clientes = Cliente.objects.all().exclude(activo = False)
    cliente_form = ClienteForm()
    reporte = Configuracion.objects.all().last()
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)

        if cliente_form.is_valid():
            cliente_form.save()
            messages.success(request, 'Sea agregó correctamente el cliente')
            cliente_form = ClienteForm()
            return render (request, 'cliente/index_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'clientes':clientes,'cliente_form':cliente_form})
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
    return render (request, 'cliente/index_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'reporte':reporte,'clientes':clientes,'cliente_form':cliente_form})

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
    auditoria =  Cliente.history.all()
    return render(request, 'auditoria_cliente.html',{'envios_not':envios_not,'envio_count':envio_count,'auditoria':auditoria, 'reporte':reporte})

#Ver Cambios
def VerAuditoria(request,pk,id_history):
    historial = Cliente.history.filter(dni=pk)
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
