from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import Tipo_materialForm, MaterialForm, Unidad_medidaForm, CompraForm
from .models import Tipo_material, Material, Unidad_medida, Compra
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from config.models import Configuracion

from apps.prenda.models import Ingrediente
from apps.pedido.models import Faltante, Pedido, Detalle_envio

import json
from django.http import HttpResponse
from django.http import JsonResponse

#Crear un tipo de tipo_material
def CrearTipo_material (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    tipo_materiales = Tipo_material.objects.all()
    if request.method == 'POST':
        if 'boton_guardar_listar' in request.POST:
            tipo_material_form = Tipo_materialForm(request.POST)
            if tipo_material_form.is_valid():
                try:
                    tipo_material_form.save()
                    messages.success(request, 'Se creó un tipo de material')
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            return ListarTipo_material(request)
        if 'boton_guardar_agregar' in request.POST:
            tipo_material_form = Tipo_materialForm(request.POST)
            if tipo_material_form.is_valid():
                try:
                    tipo_material_form.save()
                    messages.success(request, 'Se creó un tipo de material')
                except Exception as e:
                    messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            return redirect('/material/crear_tipo_material')
    else:
        tipo_material_form = Tipo_materialForm()
    return render(request, 'material/crear_tipo_material.html',{'envios_not':envios_not,'envio_count':envio_count,'envios_not':envios_not,'envio_count':envio_count,'tipo_materiales':tipo_materiales,'tipo_material_form':tipo_material_form})
#Listar todos los tipo_materiales
def ListarTipo_material (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    tipo_materiales = Tipo_material.objects.all()
    return render(request,'material/listar_tipo_material.html',{'envios_not':envios_not,'envio_count':envio_count,'tipo_materiales':tipo_materiales})
#Editar un tipo_material
def EditarTipo_material (request,id_tipo_material):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    tipo_materiales = Tipo_material.objects.all()
    tipo_material_form=None
    tipo_material = Tipo_material.objects.get(id_tipo_material=id_tipo_material)
    if request.method=='GET':
        tipo_material_form=Tipo_materialForm(instance=tipo_material)
    else:
        tipo_material_form=Tipo_materialForm(request.POST, instance=tipo_material)
        if tipo_material_form.is_valid():
            tipo_material_form.save()
            messages.success(request, 'Se editó el tipo de material')
            return ListarTipo_material(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de editar el tipo de material')
    return render(request,'material/editar_tipo_material.html',{'envios_not':envios_not,'envio_count':envio_count,'tipo_materiales':tipo_materiales,'tipo_material_form':tipo_material_form})

#Eliminar un cliente
def EliminarTipo_material (request,id_tipo_material):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    tipo_material = get_object_or_404(Tipo_material,id_tipo_material=id_tipo_material)
    try:
        tipo_material.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el tipo de material')
    tipo_materiales = Tipo_material.objects.all()
    return render(request,'material/listar_tipo_material.html',{'envios_not':envios_not,'envio_count':envio_count,'tipo_material':tipo_material,'tipo_materiales':tipo_materiales})

#Crear un material
def CrearMaterial (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    materiales = Material.objects.all()
    if request.method == 'POST':
        if 'boton_guardar_listar' in request.POST:
            material_form = MaterialForm(request.POST)
            if material_form.is_valid():
                material_form.save()
                messages.success(request, 'Se creó correctamente el material')
                return ListarMaterial(request)
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el material')
        if 'boton_guardar_agregar' in request.POST:
            material_form = MaterialForm(request.POST)
            if material_form.is_valid():
                material_form.save()
                messages.success(request, 'Se creó correctamente el material')
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el material')
            return redirect ('/material/crear_material')
    else:
        material_form = MaterialForm()
    return render(request, 'material/crear_material.html',{'envios_not':envios_not,'envio_count':envio_count,'materiales':materiales,'material_form':material_form})
#Listar todos los materiales
def ListarMaterial (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    materiales = Material.objects.all()
    reporte = Configuracion.objects.all().last()
    return render(request,'material/listar_material.html',{'envios_not':envios_not,'envio_count':envio_count,'reporte':reporte,'materiales':materiales})
#Editar un material
def EditarMaterial (request,id_material):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    materiales = Material.objects.all()
    try:
        error = None
        material_form=None
        material = Material.objects.get(id_material=id_material)
        if request.method=='GET':
            material_form=MaterialForm(instance=material)
        else:
            if 'boton_guardar_listar' in request.POST:
                material_form=MaterialForm(request.POST, instance=material)
                if material_form.is_valid():
                    material_form.save()
                    return ListarMaterial(request)
            if 'boton_guardar_agregar' in request.POST:
                material_form=MaterialForm(request.POST, instance=material)
                if material_form.is_valid():
                    material_form.save()
                return redirect ('/material/crear_material')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/editar_material.html',{'envios_not':envios_not,'envio_count':envio_count,'materiales':materiales,'material_form':material_form, 'error':error})
#Eliminar un material
def EliminarMaterial (request,id_material):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    material = get_object_or_404(Material,id_material=id_material)
    try:
        material.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el material')
    messages.warning(request, 'Se eliminó el material correctamente')
    materiales = Material.objects.all()
    return redirect('/material/listar_material')

#Crear una unidad de medida
def CrearUnidad_medida (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    unidad_medidas = Unidad_medida.objects.all()
    if request.method == 'POST':
        if 'boton_guardar_listar' in request.POST:
            unidad_medida_form = Unidad_medidaForm(request.POST)
            if unidad_medida_form.is_valid():
                unidad_medida_form.save()
                return ListarUnidad_medida(request)
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear la unidad de medida')
        if 'boton_guardar_agregar' in request.POST:
            unidad_medida_form = Unidad_medidaForm(request.POST)
            if unidad_medida_form.is_valid():
                unidad_medida_form.save()
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear la unidad de medida')
            return redirect('/material/crear_unidad_medida')
    else:
        unidad_medida_form = Unidad_medidaForm()
    return render(request, 'material/crear_unidad_medida.html',{'envios_not':envios_not,'envio_count':envio_count,'unidad_medidas':unidad_medidas,'unidad_medida_form':unidad_medida_form})
#Listar todos las unidad_medidas
def ListarUnidad_medida (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    unidad_medidas = Unidad_medida.objects.all()
    return render(request,'material/listar_unidad_medida.html',{'envios_not':envios_not,'envio_count':envio_count,'unidad_medidas':unidad_medidas})
#Editar un unidad_medida
def EditarUnidad_medida (request,id_unidad):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    unidad_medida = Unidad_medida.objects.get(id_unidad=id_unidad)
    unidad_medidas = Unidad_medida.objects.all()
    if request.method=='GET':
        unidad_medida_form=Unidad_medidaForm(instance=unidad_medida)
    else:
        unidad_medida_form=Unidad_medidaForm(request.POST, instance=unidad_medida)
        if unidad_medida_form.is_valid():
            unidad_medida_form.save()
        return ListarUnidad_medida(request)
    return render(request,'material/editar_unidad_medida.html',{'envios_not':envios_not,'envio_count':envio_count,'unidad_medidas':unidad_medidas,'unidad_medida_form':unidad_medida_form})
#Eliminar un unidad_medida
def EliminarUnidad_medida (request,id_unidad):
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
        unidad_medida = get_object_or_404(Unidad_medida,id_unidad=id_unidad)
        unidad_medida.delete()
        messages.warning(request, 'Se eliminó la unidad de medida')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar la unidad de medida')
    return ListarUnidad_medida(request)

#Registrar una compra
def CrearCompra (request):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    materiales = Material.objects.all()
    compras = Compra.objects.all()
    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        usuario = request.user #Obtengo el usuario registrado actualmente
        if compra_form.is_valid():
            compra = compra_form.save(commit=False) #Registro la compra
            compra.usuario = usuario
            compra.save()
            id_material = request.POST['material'] #Obtengo el id del material involucrado
            cantidad = request.POST['cantidad'] #Obtengo la cantidad de la compra registrada
            material = Material.objects.get(id_material=id_material) #Obtengo el material
            material.stock=material.stock + int(cantidad) #Sumo la cantidad al stock actual
            cantidad = int(cantidad)

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
            material.save() #Se actualiza el stock del material

            return redirect('/material/crear_compra')
    else:
        compra_form = CompraForm()
    return render(request, 'material/crear_compra.html',{'envios_not':envios_not,'envio_count':envio_count,'compras':compras,'materiales':materiales,'compra_form':compra_form})
#Listar todos las compras
def ListarCompra (request):
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
    compras = Compra.objects.all()
    return render(request,'material/listar_compra.html',{'envios_not':envios_not,'envio_count':envio_count,'compras':compras,'reporte':reporte})
#Editar un compra
def EditarCompra (request,id_compra):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    compra = Compra.objects.get(pk = id_compra)
    if request.method=='POST':
        compra_form=CompraForm(request.POST, instance=compra)
        print("------")
        print(request.POST)
        if compra_form.is_valid():
            compra = compra_form.save()
            compra.usuario = request.user
            compra.save()
            print("ENTRAONOpost")
            print(compra.cantidad)
            return redirect('/material/crear_compra/')
    else:
        compra_form=CompraForm(instance=compra)

    return render(request,'material/editar_compra.html',{'envios_not':envios_not,'envio_count':envio_count,'compra_form':compra_form})
#Eliminar un compra
def EliminarCompra (request,id_compra):
    #Notificaciones
    pedidos = Pedido.objects.all().exclude(confirmado=False)
    envios_noti = []
    for pedido in pedidos:
        envio_temp = Detalle_envio.objects.filter(pedido = pedido).exclude(visto=True).first()
        if envio_temp:
            envios_noti.append(envio_temp)
    envios_not = envios_noti[:3]
    envio_count = len(envios_noti)

    compra = Compra.objects.get(id_compra=id_compra) #Obtengo la compra
    material = compra.material #Obtengo el material de la compra
    material.stock -= compra.cantidad #Resto la cantidad comprada al stock del material
    material.save() #Actualizo el stock
    compra.delete() #Elimino la compra
    messages.warning(request, 'Se eliminó la compra correctamente') #Informo que la transaccion fue exitosa
    return redirect('material:crear_compra') #Redirecciono a la lista de materiales

#Mostrar unidad de medida al asignar material
def MostrarUnidad(request):
    mt = request.GET.get('material',None)
    tipo_material = Tipo_material.objects.get(id_tipo_material = mt)
    unidad = tipo_material.unidad_medida.nombre
    result = {
        'medida': unidad
    }
    print(result)
    return JsonResponse(result)
