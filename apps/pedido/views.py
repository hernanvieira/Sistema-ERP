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
from config.models import Configuracion, ConfiguracionMensaje
from django.core.mail import EmailMessage

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
    return render(request, 'pedido/crear_pedido.html',{'pedido_form':pedido_form, 'cliente_form':cliente_form})

#Listar todos los pedidos
def ListarPedido (request):
    pedidos = Pedido.objects.all()
    reporte = Configuracion.objects.all().last()
    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux
    return render(request,'pedido/listar_pedido.html',{'reporte':reporte,'pedidos':pedidos})

def ListarPedido2 (request,id_pedido):
    pedidos = Pedido.objects.all()
    reporte = Configuracion.objects.all().last()
    aux = []
    for p in pedidos:
        if Estado_pedido.objects.filter(pedido=p).exists():
            a = Estado_pedido.objects.filter(pedido = p).order_by('-id_estado_pedido')[0]
            aux.append(a)
    pedidos = aux
    return render(request,'pedido/listar_pedido.html',{'id_pedido':id_pedido,'reporte':reporte,'pedidos':pedidos})

#Volver al pedido
def VolverPedido (request,id_pedido):
        detalles = None
        pedido_form=None
        pedido = Pedido.objects.get(id_pedido=id_pedido)
        pedido_id = pedido.id_pedido
        detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
        mensaje = ConfiguracionMensaje.objects.all().last()
        reporte = Configuracion.objects.all().last()

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

                print("FINALIZAAAAAAAAAAAAAAAAAAA")
                id_pedido = pedido.id_pedido
                print("MIRA ELN NUMERITO")
                print(id_pedido)

                if pedido.seña != None:
                    pedido.save()
                    estado_pedido.save()
                    messages.success(request, 'Todo ocurrió correctamente')
                    return redirect('/pedido/listar_pedido/'+str(id_pedido))

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
    mensaje = ConfiguracionMensaje.objects.all().last()
    cliente = pedido.cliente
    detalles = Detalle.objects.filter(pedido_id=id_pedido).select_related('prenda')
    estados = Estado_pedido.objects.filter(pedido_id=id_pedido)
    if Estado_pedido.objects.filter(pedido_id=id_pedido).exists():
        estado = Estado_pedido.objects.filter(pedido_id=id_pedido).order_by('-id_estado_pedido')[0]
    else:
        estado = None
    if request.method=='GET':
        pedido_form=PedidoForm(instance=pedido)
    else:
        if 'boton_cancelar' in request.POST:
            CancelarPedido(request,id_pedido)
        if 'boton_entregar' in request.POST:
            EntregarPedido(request,id_pedido)
        if 'boton_registrar_entega' in request.POST:
            peticion = request.POST.copy()
            peticion_valor = peticion.pop('registrar_entrega')[0]
            pedido.entrega += int(peticion_valor)

            saldo = pedido.precio_total - pedido.entrega
            if saldo == 0:
                pedido.save()
                messages.success(request, 'Se registró la entrega y se completó el pago')

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: $0,00' , to=[pedido.cliente.correo])
                email.send()

            if saldo > 0:
                pedido.save()
                messages.success(request, 'Se registró la entrega, resta un saldo de: ' + str(saldo))

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: ' + str(saldo), to=[pedido.cliente.correo])
                email.send()

            if saldo < 0:
                pedido.entrega = pedido.precio_total
                pedido.save()
                messages.success(request, 'Se registró la entrega y se completó el pago. El cambio es de: ' + str(abs(saldo)))

                email = EmailMessage('PROYECTO SOFTWARE', mensaje.entrega + ' El saldo es de: $0,00' , to=[pedido.cliente.correo])
                email.send()

            if pedido.entrega >= pedido.seña:
                estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
                estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
                estado_en_produccion = Estado.objects.get(id_estado = 2) #Obtengo el estado "En produccion"

                estado = Estado_pedido.objects.filter(pedido_id=id_pedido).order_by('-id_estado_pedido')[0]

                if estado.estado != estado_en_produccion: #Si no estaba en produccion

                    estado_pedido.estado = estado_en_produccion #Asocio el estado "En produccion"
                    estado_pedido.pedido = pedido # Asocio el pedido actual
                    estado_pedido.fecha = datetime.date.today() #Establezco como fecha el dia de hoy

                    estado_pedido.save()#Guardo el estado

                    email = EmailMessage('PROYECTO SOFTWARE', mensaje.en_produccion, to=[pedido.cliente.correo])
                    email.send()

        pedido_form=PedidoForm(instance=pedido)
        if Estado_pedido.objects.filter(pedido_id=id_pedido).exists():
            estado = Estado_pedido.objects.filter(pedido_id=id_pedido).order_by('-id_estado_pedido')[0]
        else:
            estado = None
    return render(request,'pedido/ver_pedido.html',{'cliente':cliente,'pedido_form':pedido_form,'detalles':detalles, 'estado':estado,'pedido':pedido,'estados':estados})


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
    mensaje = ConfiguracionMensaje.objects.all().last()

    estado_cancelado = Estado.objects.get(id_estado = 5)

    estado_pedido.estado = estado_cancelado
    estado_pedido.pedido = pedido
    estado_pedido.fecha = datetime.date.today()

    pedido.save()
    estado_pedido.save()
    messages.warning(request, 'Se canceló el pedido')

    # Envio de correo
    email = EmailMessage('PROYECTO SOFTWARE', mensaje.cancelado, to=[pedido.cliente.correo])
    email.send()

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

#Finalizar un pedido
def FinalizarPedido (request,id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
    estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
    estado_finalizado = Estado.objects.get(id_estado = 3) #Obtengo el estado "Finalizar"
    mensaje = ConfiguracionMensaje.objects.all().last()


    estado_pedido.estado = estado_finalizado #Asocio el estado "En produccion"
    estado_pedido.pedido = pedido # Asocio el pedido actual
    estado_pedido.fecha = datetime.date.today() #Establezco como fecha el dia de hoy

    estado_pedido.save()#Guardo el estado
    pedido.save()
    estado_pedido.save()
    messages.success(request, 'Se finalizó el pedido')

    email = EmailMessage('PROYECTO SOFTWARE', mensaje.finalizado, to=[pedido.cliente.correo])
    email.send()

    return redirect('/pedido/ver_pedido/' + str(id_pedido))

#Entregar un pedido
def EntregarPedido (request,id_pedido):
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    estado_pedido_form = Estado_pedidoForm() #Creo una instancia de formulario para crear el estado
    estado_pedido = estado_pedido_form.save(commit = False) #Guardo con Commit = False para asociar el pedido
    estado_entregado = Estado.objects.get(id_estado = 4) #Obtengo el estado "Finalizar"
    mensaje = ConfiguracionMensaje.objects.all().last()

    estado_pedido.estado = estado_entregado #Asocio el estado "En produccion"
    estado_pedido.pedido = pedido # Asocio el pedido actual
    estado_pedido.fecha = datetime.date.today() #Establezco como fecha el dia de hoy

    estado_pedido.save()#Guardo el estado
    pedido.save()
    estado_pedido.save()
    messages.success(request, 'Se entregó el pedido')

    email = EmailMessage('PROYECTO SOFTWARE', mensaje.entregado, to=[pedido.cliente.correo])
    email.send()

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
    auditoria =  Pedido.history.all()
    return render(request, 'auditoria_pedido.html',{'auditoria':auditoria})
