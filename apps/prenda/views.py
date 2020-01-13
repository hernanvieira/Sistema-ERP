from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import MedidaForm, Tipo_prendaForm, PrendaForm, IngredienteForm, DetalleForm, Medida_prendaForm
from .models import Tipo_prenda, Prenda, Ingrediente, Medida, Medida_prenda
from apps.material.models import Material, Tipo_material
from apps.pedido.models import Pedido, Detalle, Faltante
# from apps.prenda.models import Faltante
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import datetime, timedelta
from decimal import Decimal


#JSON
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

import json
from django.http import HttpResponse
from django.http import JsonResponse

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def _init_(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self)._init_(content, **kwargs)


#Crear un Medida
def CrearMedida (request):
    medidas = Medida.objects.all()
    if request.method == 'POST':
        medida_form = MedidaForm(request.POST)
        if medida_form.is_valid():
            if "boton_crear_agregar" in request.POST:
                medida = medida_form.save()
                medidas = Medida.objects.all()
                return render(request, 'prenda/crear_medida.html',{'medidas':medidas, 'medida_form':medida_form})
            medida = medida_form.save()
            return ListarMedida(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de crear la medida')
    else:
        medida_form = MedidaForm()
        medidas = Medida.objects.all()
    return render(request, 'prenda/crear_medida.html',{'medidas':medidas, 'medida_form':medida_form})
#Listar todos las medidas
def ListarMedida (request):
    medidas = Medida.objects.all()
    return render(request,'prenda/listar_medida.html',{'medidas':medidas})
#Editar una medida
def EditarMedida (request,id_medida):
    try:
        error = None
        medida_form=None
        medida = Medida.objects.get(id_medida=id_medida)
        if request.method=='GET':
            medida_form=MedidaForm(instance=medida)
        else:
            medida_form=MedidaForm(request.POST, instance=medida)
            if medida_form.is_valid():
                medida_form.save()
            return ListarMedida(request)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/editar_medida.html',{'medida_form':medida_form, 'error':error})
#Eliminar una medida
def EliminarMedida (request,id_medida):
    medida = get_object_or_404(Medida, id_medida=id_medida)
    try:
        medida.delete()
        messages.warning(request, 'Se eliminó la medida')
    except Exception as e:
        messages.error(request, "Ocurrió un error al tratar de eliminar la medida " + str(id_pedido))
    return ListarMedida(request)

#Crear un tipo de prenda
def CrearTipo_prenda (request):
    tipo_prendas = Tipo_prenda.objects.all()
    if request.method == 'POST':
        tipo_prenda_form = Tipo_prendaForm(request.POST)
        if tipo_prenda_form.is_valid():
            if "boton_crear_agregar" in request.POST:
                tipo_prenda_form.save()
                return render(request, 'prenda/crear_tipo_prenda.html',{'tipo_prendas': tipo_prendas, 'tipo_prenda_form':tipo_prenda_form})
            tipo_prenda_form.save()
            return ListarTipo_prenda(request)
        else:
            messages.error(request,"Ocurrió un error al crear el tipo de prenda")

    else:
        tipo_prenda_form = Tipo_prendaForm()
    return render(request, 'prenda/crear_tipo_prenda.html',{'tipo_prendas': tipo_prendas, 'tipo_prenda_form':tipo_prenda_form})
#Listar todos los tipos de prendas
def ListarTipo_prenda (request):
    tipo_prendas = Tipo_prenda.objects.all()
    return render(request,'prenda/listar_tipo_prenda.html',{'tipo_prendas':tipo_prendas})
#Editar un tipo de prenda
def EditarTipo_prenda (request,id_tipo_prenda):
    tipo_prendas = Tipo_prenda.objects.all()
    try:
        tipo_prenda_form=None
        tipo_prenda = Tipo_prenda.objects.get(id_tipo_prenda=id_tipo_prenda)
        if request.method=='GET':
            tipo_prenda_form=Tipo_prendaForm(instance=tipo_prenda)
        else:
            tipo_prenda_form=Tipo_prendaForm(request.POST, instance=tipo_prenda)
            if tipo_prenda_form.is_valid():
                tipo_prenda_form.save()
            return ListarTipo_prenda(request)
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/editar_tipo_prenda.html',{'tipo_prendas':tipo_prendas,'tipo_prenda_form':tipo_prenda_form})
#Ver tipo de prenda
def VerTipo_prenda (request,id_tipo_prenda):
    try:
        error = None
        tipo_prenda_form=None
        tipo_prenda = Tipo_prenda.objects.get(id_tipo_prenda=id_tipo_prenda)
        medidas = tipo_prenda.medida.all()
        if request.method=='GET':
            tipo_prenda_form=Tipo_prendaForm(instance=tipo_prenda)
        else:
            tipo_prenda_form=Tipo_prendaForm(request.POST, instance=tipo_prenda)
            if tipo_prenda_form.is_valid():
                tipo_prenda_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/ver_tipo_prenda.html',{'tipo_prenda_form':tipo_prenda_form, 'medidas':medidas, 'error':error})
#Eliminar un tipo de prenda
def EliminarTipo_prenda (request,id_tipo_prenda):
    tipo_prenda = get_object_or_404(Tipo_prenda, id_tipo_prenda=id_tipo_prenda)
    try:
        tipo_prenda.delete()
        messages.warning(request, 'Se eliminó el tipo de prenda')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el estado')
    return ListarTipo_prenda(request)
#Registrar una prenda al detalle
def CrearPrenda (request,id_pedido):
    if request.method == 'POST':
        prenda_form = PrendaForm(request.POST)
        detalle_form = DetalleForm(request.POST)
        pedido = Pedido.objects.get(id_pedido = id_pedido) #obtendo el pedido
        cliente = pedido.cliente

        reputacion = abs((int(cliente.reputacion)/100)-1)
        if cliente.reputacion < 0:
            reputacion = 0
        if cliente.reputacion > 100:
            reputacion = 1

        print("EKEKEKEKEKE")
        print(cliente.reputacion)
        print(reputacion)

        if prenda_form.is_valid() and detalle_form.is_valid():
            prenda = prenda_form.save(commit = False) #Guardo prenda
            prenda.imagen = request.FILES.get('txtImagen')
            prenda.save()

            detalle = detalle_form.save() #Guardo detalle
            detalle.tiempo_prod_lote = detalle.cantidad * prenda.tiempo_prod_prenda #Calculo el tiempo de produccion por lote
            tiempo = detalle.tiempo_prod_lote
            detalle.save() #Actualizo el detalle
            pedido.precio_total += prenda.precio * detalle.cantidad #Calculo precio total
            pedido.seña = pedido.precio_total*Decimal(reputacion)

            fecha = Pedido.objects.exclude(fecha_entrega=None).order_by('fecha_entrega')
            fechona  = fecha.last()
            print("LA ULTIMA FECHARDA")
            print(fechona.fecha_entrega)
            print("SE LE SUMA")
            print(tiempo)
            pedido.fecha_entrega = fechona.fecha_entrega + timedelta(days= tiempo)
            print("Nueva fechona")
            print(pedido.fecha_entrega)

            # Asocio datos de prenda y pedido a detalle
            detalle.prenda = prenda
            detalle.pedido = pedido
            pedido.save() # Actualizo el pedido
            detalle.save() # Actualizo el detalle
            id_detalle = detalle.id_detalle #Obtengo el id del detalle
            if 'boton_asignar_material' in request.POST:
                prenda_form=PrendaForm(request.POST, instance=prenda)
                if prenda_form.is_valid():
                    prenda_form.save() #Guardo prenda
                ingrediente_form = IngredienteForm()
                return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
            if 'boton_asignar_medida' in request.POST:
                prenda_form=PrendaForm(request.POST, instance=prenda)
                if prenda_form.is_valid():
                    prenda_form.save() #Guardo prenda
                medida_prenda_form = Medida_prendaForm()
                return redirect('/prenda/asignar_medida/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'medida_prenda_form':medida_prenda_form})
            return redirect('/pedido/volver_pedido/'+str(id_pedido))
        else:
            messages.error(request, 'Ocurrió un error al tratar de agregar una prenda')
    else:
        prenda_form = PrendaForm()
        detalle_form = DetalleForm()
        medida_prenda_form = Medida_prendaForm()
        pedido = Pedido.objects.get(id_pedido = id_pedido) #obtendo el pedido
        medidas_prenda = Medida.objects.all()
    medidas_prenda = Medida.objects.all()
    medida_prenda_form = Medida_prendaForm()
    return render(request, 'prenda/crear_prenda.html',{'medidas_prenda':medidas_prenda,'prenda_form':prenda_form,'detalle_form':detalle_form,'pedido':pedido, 'medida_prenda_form':medida_prenda_form})
#Listar todos las prendas
def ListarPrenda (request):
    prendas = Prenda.objects.all()
    return redirect('index')
#Editar una prenda
def EditarPrenda (request,id_prenda,id_detalle,id_pedido):
    redireccionar = 0
    prenda_form=None
    detalle_form=None
    prenda = Prenda.objects.get(id_prenda=id_prenda)
    detalle = Detalle.objects.get(id_detalle=id_detalle)

    cant_pre = detalle.cantidad
    print("Cantidad prenda actual: " + str(cant_pre))

    pedido = Pedido.objects.get(id_pedido=id_pedido)
    cantidad_pre = detalle.cantidad #Obtengo la cantidad previo a editar
    precio_pre = prenda.precio #Obtengo el precio previo a editar
    tpp_pre = prenda.tiempo_prod_prenda #Obtengo el tiempo pp previo a editar
    if request.method=='GET':
        prenda_form=PrendaForm(instance=prenda)
        detalle_form=DetalleForm(instance=detalle)
    else:
        prenda_form=PrendaForm(request.POST, instance=prenda)
        detalle_form=DetalleForm(request.POST, instance=detalle)
        if prenda_form.is_valid() and detalle_form.is_valid():
            prenda = prenda_form.save(commit = False) #Guardo prenda
            if request.FILES:
                prenda.imagen = request.FILES.get('txtImagen')
            prenda.save()
            detalle = detalle_form.save() #Guardo detalle

            if prenda.precio != precio_pre or detalle.cantidad != cantidad_pre: #Si cambia la cantidad o el precio unitario
                precio_total_pre = precio_pre * cantidad_pre #Obtengo el precio total anterior
                precio_pos = prenda.precio * detalle.cantidad - precio_total_pre #Calculo el precio del lote actualizado
                pedido.precio_total += precio_pos #Actualizo el precio total
                pedido.seña = pedido.precio_total/2 #Actualizo la seña
                detalle.tiempo_prod_lote = detalle.cantidad * prenda.tiempo_prod_prenda #Calculo el tiempo de produccion por lote

            #Asocio datos de prenda y pedido a detalle
            detalle.prenda = prenda
            detalle.pedido = pedido

            pedido.save() # Actualizo el pedido
            detalle.save() # Actualizo el detalle

            cant_post = detalle.cantidad
            print("Cantidad prenda nueva: " + str(cant_post))
            ingredientes = Ingrediente.objects.filter(prenda_id = prenda.id_prenda)
            print(ingredientes)
            for ingre in ingredientes:
                mat_pre = cant_pre * ingre.cantidad
                mat_post = cant_post * ingre.cantidad
                print("Cantidad material previo: " + str(mat_pre))
                print("Cantidad material nuevo: " + str(mat_post))
                cant_dif = mat_post - mat_pre
                print("Diferencia de cantidad: " + str(cant_dif))
                material = Material.objects.get(id_material = ingre.material_id)
                print(material.nombre)

                if cant_dif <= material.stock:
                    print("Hay stock disponible")
                else:
                    print("No hay stock disponible")
                    redireccionar = 1
                    messages.error(request, 'No hay stock disponible para el material ' + str(material)) # Informo que no hay stock para dicho material
            print(redireccionar)

            if redireccionar == 1:
                detalle.cantidad = cantidad_pre
                detalle.save()
                return redirect('/prenda/editar_prenda/'+str(id_prenda)+'/'+ str(id_detalle)+'/'+str(id_pedido))
            id_detalle = detalle.id_detalle #Obtengo el id del detalle
            if 'boton_asignar_material' in request.POST:
                ingrediente_form = IngredienteForm()
                return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
            if 'boton_asignar_medida' in request.POST:
                prenda_form=PrendaForm(request.POST, instance=prenda)
                if prenda_form.is_valid():
                    prenda_form.save() #Guardo prenda
                medida_prenda_form = Medida_prendaForm()
                return redirect('/prenda/asignar_medida/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'medida_prenda_form':medida_prenda_form})
            if redireccionar == 0:

                for ingre in ingredientes:
                    mat_pre = cant_pre * ingre.cantidad
                    mat_post = cant_post * ingre.cantidad
                    print("Cantidad material previo: " + str(mat_pre))
                    print("Cantidad material nuevo: " + str(mat_post))
                    cant_dif = mat_post - mat_pre
                    print("Diferencia de cantidad: " + str(cant_dif))
                    material = Material.objects.get(id_material = ingre.material_id)
                    print(material.nombre)

                    #Actualizar stock
                    material.stock -= cant_dif # Actualizo el stock
                    material.save() # persisto

                return redirect('/pedido/volver_pedido/'+str(id_pedido))

    return render(request,'prenda/editar_prenda.html',{'prenda_form':prenda_form,'detalle_form':detalle_form, 'pedido':pedido, 'prenda':prenda})
#Eliminar un cliente
def EliminarPrenda(request,id_prenda, id_detalle, id_pedido):
    prenda = get_object_or_404(Prenda,id_prenda=id_prenda)
    detalle = get_object_or_404(Detalle, id_detalle=id_detalle)
    pedido = get_object_or_404(Pedido, id_pedido=id_pedido)
    # try:
    pedido.precio_total = (pedido.precio_total) - (prenda.precio * detalle.cantidad) #Actualizo el precio total
    pedido.seña = pedido.precio_total/2 #Actualizo la seña minima
    pedido.save() # Actualizo el pedido
    detalle.delete() #Elimino el detalle
    prenda.delete() #Elimino la prenda
    # except Exception as e:
        # messages.error(request, 'Ocurrió un error al tratar de eliminar el clientela prenda')
    return redirect('/pedido/volver_pedido/'+str(id_pedido))

#Asigna un material a la prenda
def AsignarMaterial(request,id_prenda,id_detalle,id_pedido):
    prenda = Prenda.objects.get(id_prenda=id_prenda)
    pedido = Pedido.objects.get(id_pedido = id_pedido)
    detalle = Detalle.objects.get(id_detalle = id_detalle)
    if request.method == 'POST':
        ingrediente_form = IngredienteForm(request.POST)
        prenda = Prenda.objects.get(id_prenda=id_prenda)
        detalle = Detalle.objects.get(id_detalle=id_detalle)

        if ingrediente_form.is_valid():
            ingrediente = ingrediente_form.save(commit = False) #guardo el ingrediente
            material = ingrediente.material # obtengo el material

            # Obtener Unidad de medida
            tipo_material = Tipo_material.objects.get(material = material)
            unidad_medida = tipo_material.unidad_medida

            cantidad_material = ingrediente.cantidad * detalle.cantidad # obtengo la cant. material multiplicando el ingrediente por la cantidad de unidades solicitadas
            ingrediente.cantidadxdetalle = cantidad_material
            if cantidad_material < material.stock: # Si la cantidad solicitada es menor al stock disponible
                material_post = material.stock - cantidad_material # calculo con cuanto stock quedaría

                #Actualizar stock
                material.stock -= cantidad_material # Actualizo el stock
                material.save() # persisto
                #Guardo la asignación de material
                ingrediente.prenda = prenda # asocio el material con la prenda

                mat_prenda = Ingrediente.objects.filter(prenda = prenda, material = material).exists()#Existe ese material entre los ingredientes ingresados?
                if mat_prenda:# si existe
                    ingre = Ingrediente.objects.get(prenda = prenda, material = material)# Obtengo el ingrediente
                    ingre.cantidad += ingrediente.cantidad #sumo la nueva cantidad a la actual
                    ingre.save() # actualizo el ingrediente
                else:
                    ingrediente.save() #persisto

                #Actualizo el detalle
                detalle.prenda = prenda # Asocio la prenda con el detalle
                detalle.pedido = pedido # Asocio el pedido con el detalle
                detalle.save() #Persisto
                messages.success(request, 'Se asignó el material') # Informo que se asignó correctamente
                if material_post > material.stock_minimo:
                    if 'boton_guardar_cargar' in request.POST:
                        return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
                    return redirect('/prenda/editar_prenda/'+str(id_prenda)+'/'+str(id_detalle)+'/'+str(id_pedido))
                else:
                    messages.warning(request, 'La cantidad introducida supera el stock mínimo')
                    if 'boton_guardar_cargar' in request.POST:
                        return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
                    return redirect('/prenda/editar_prenda/'+str(id_prenda)+'/'+str(id_detalle)+'/'+str(id_pedido))
            else:
                material_post = material.stock - cantidad_material #Calculo cuanto material necesito a parte del stock que tengo

                faltante = Faltante.objects.create(tipo_material = material.tipo_material, material = material, faltante = abs(material_post), prenda = prenda, pedido = pedido) # Creo el objeto faltante

                #Guardo la asignación de material
                ingrediente.prenda = prenda # asocio el material con la prenda

                mat_prenda = Ingrediente.objects.filter(prenda = prenda, material = material).exists()#Existe ese material entre los ingredientes ingresados?
                if mat_prenda:# si existe
                    ingre = Ingrediente.objects.get(prenda = prenda, material = material)# Obtengo el ingrediente
                    ingre.cantidad += ingrediente.cantidad #sumo la nueva cantidad a la actual
                    ingre.save() # actualizo el ingrediente
                else:
                    ingrediente.save() #persisto

                #Actualizo el detalle
                detalle.prenda = prenda # Asocio la prenda con el detalle
                detalle.pedido = pedido # Asocio el pedido con el detalle
                detalle.save() #Persisto
                messages.success(request, 'Se asignó el material') # Informo que se asignó correctamente

                pedido.fecha_entrega += timedelta(days=material.tiempo_reposicion) #Sumo el tiempo de resposicion estimado del material faltante
                pedido.save() # Actualizo el pedido

                messages.error(request, 'La cantidad introducida es mayor al stock disponible xd')
                return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
    else:
        ingrediente_form = IngredienteForm()
    ingredientes = Ingrediente.objects.filter(prenda_id = id_prenda)
    lista = []
    for ingrediente in ingredientes:
        material = ingrediente.material
        cantidad = ingrediente.cantidadxdetalle

        cantidad = detalle.cantidad * ingrediente.cantidad

        if cantidad <= material.stock:
            ingrediente.disponibilidad = "Disponible"
            cant_post = material.stock - cantidad
            if cant_post >= material.stock_minimo:
                ingrediente.disponibilidad = "Disponible"
            else:
                ingrediente.disponibilidad = "Stock Minimo"
        else:
            ingrediente.disponibilidad = "Faltante"
        ingrediente.save()
        lista.append(ingrediente)
    return render(request,'prenda/asignar_material.html',{'lista':lista,'ingrediente_form':ingrediente_form,'prenda':prenda,'pedido':pedido,'ingredientes':ingredientes, 'detalle':detalle})

#Asignar medidas a la prenda
def AsignarMedida(request,id_prenda,id_detalle,id_pedido):
    pedido = Pedido.objects.get(id_pedido = id_pedido)
    detalle = Detalle.objects.get(id_detalle = id_detalle)
    prenda = Prenda.objects.get(id_prenda=id_prenda) # Obtengo la prenda a la que voy a asociar las medida
    medidas_prenda = Medida.objects.filter(tipo_prenda = prenda.tipo_prenda) #Obtengo las medidas asociadas a ese tipo de prenda
    medidas_prenda_u = Medida_prenda.objects.filter(prenda_id = id_prenda) # Obtengo los valores de las medidas si ya fueron cargadas ateriormente
    medida_prenda_form = Medida_prendaForm() # Intancio un formulario para cargar medidas
    a = []
    b =[]
    c = False
    for m in medidas_prenda:
        b.append(m)

    if medidas_prenda_u:
        for m in medidas_prenda_u:
            a.append(m.medida)

        if a == b:
            c = True
        else:
            c = False

    if request.method == 'POST': # si el metodo es POST
        if medidas_prenda_u and c == True:
            peticion = request.POST.copy() # OBtengo una copia del request
            peticion_valor = peticion.pop('valor_medida') # Obtengo los valores de cada medida
            i=0
            for m in medidas_prenda_u:
                m.valor = peticion_valor[i]
                i+=1
                m.save()
            messages.success(request, 'Medidas actualizadas correctamente') # Informo al usuario que se creó correctamente
            return redirect('/prenda/editar_prenda/'+str(id_prenda)+'/'+str(id_detalle)+'/'+str(id_pedido))
        else:
            if medidas_prenda_u:
                for m in medidas_prenda_u:
                    m.delete()
            medida_prenda_form = Medida_prendaForm(request.POST) # Intancio el formulario con los datos de la pagina
            peticion = request.POST.copy() # OBtengo una copia del request
            peticion_medida = peticion.pop('medida') # Obtengo las medidas
            peticion_valor = peticion.pop('valor_medida') # Obtengo los valores de cada medida
            if medida_prenda_form.is_valid(): # si el formulario es valido
                medida = medida_prenda_form.save(commit = False) # creo un objeto del formulario para asociar las medidas y los valores

                #bucle de carga
                i=0
                while i < len(peticion_medida): # mientras haya medidas
                    if peticion_valor[i] == '': # si no se introdujo valor
                        valor = 0 # se asigna el valor 0
                    else: # si se introdujo un valor
                        valor = int(peticion_valor[i]) #se asigna el valor recibido de la peticion en esa posición
                    medida_prenda = Medida_prenda.objects.create(prenda = prenda, medida = Medida.objects.get(id_medida = peticion_medida[i]), valor = valor) # CReamos el objeto medida_prenda
                    medida_prenda.save()
                    i+=1
                #end bucle de carga
                messages.success(request, 'Medidas agregadas correctamente') # Informo al usuario que se creó correctamente
                return redirect('/prenda/editar_prenda/'+str(id_prenda)+'/'+str(id_detalle)+'/'+str(id_pedido))
    if c == False:
        medidas_prenda_u = []
    return render(request,'prenda/asignar_medida.html',{'prenda':prenda, 'pedido':pedido, 'detalle':detalle,'medidas_prenda_u':medidas_prenda_u,'medidas_prenda':medidas_prenda,'medida_prenda_form':medida_prenda_form})

def EditarMedidaPrenda(request,id_prenda):
    prenda = Prenda.objects.get(id_prenda=id_prenda)
    medidas_prenda = Medida_prenda.objects.filter(prenda_id = id_prenda)
    medida_prenda_form = Medida_prendaForm()
    if request.method == 'GET':
        medida_prenda_form = Medida_prendaForm(request.POST)
        peticion = request.POST.copy()
        peticion_medida = peticion.pop('medida')
        peticion_valor = peticion.pop('valor_medida')
        print(peticion_medida)
        print(peticion_valor)
        if medida_prenda_form.is_valid():
            medida = medida_prenda_form.save(commit = False)
            i=0
            while i < len(peticion_medida):
                if peticion_valor[i] == '':
                    valor = 0
                else:
                    valor = int(peticion_valor[i])
                medida_prenda = Medida_prenda.objects.create(prenda = prenda, medida = Medida.objects.get(id_medida = peticion_medida[i]), valor = valor)
                medida_prenda.save()
                i+=1
            messages.success(request, 'Medidas agregadas correctamente')
        else:
            print(medida_prenda_form.errors)
        return render(request,'prenda/asignar_medida.html',{'medidas_prenda':medidas_prenda,'medida_prenda_form':medida_prenda_form})

    return render(request,'prenda/asignar_medida.html',{'medidas_prenda':medidas_prenda,'medida_prenda_form':medida_prenda_form})

def VolverPrenda(request,id_pedido,id_detalle,id_prenda):
    prenda_form=None
    detalle_form=None
    prenda = Prenda.objects.get(id_prenda=id_prenda)
    detalle = Detalle.objects.get(id_detalle=id_detalle)
    pedido = Pedido.objects.get(id_pedido=id_pedido)
    cantidad_pre = detalle.cantidad #Obtengo la cantidad previo a editar
    precio_pre = prenda.precio #Obtengo el precio previo a editar
    tpp_pre = prenda.tiempo_prod_prenda #Obtengo el tiempo pp previo a editar
    if request.method=='GET':
        prenda_form=PrendaForm(instance=prenda)
        detalle_form=DetalleForm(instance=detalle)
    else:
        prenda_form=PrendaForm(request.POST, instance=prenda)
        detalle_form=DetalleForm(request.POST, instance=detalle)
        if prenda_form.is_valid() and detalle_form.is_valid():
            prenda = prenda_form.save() #Guardo prenda
            detalle = detalle_form.save() #Guardo detalle
            if 'boton_asignar_material' in request.POST:
                ingrediente_form = IngredienteForm()
                return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
            if 'boton_asignar_medida' in request.POST:
                prenda_form=PrendaForm(request.POST, instance=prenda)
                if prenda_form.is_valid():
                    prenda_form.save() #Guardo prenda
                medida_prenda_form = Medida_prendaForm()
                return redirect('/prenda/asignar_medida/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'medida_prenda_form':medida_prenda_form})
            if prenda.precio != precio_pre or detalle.cantidad != cantidad_pre: #Si cambia la cantidad o el precio unitario
                precio_total_pre = precio_pre * cantidad_pre #Obtengo el precio total anterior
                precio_pos = prenda.precio * detalle.cantidad - precio_total_pre #Calculo el precio del lote actualizado
                pedido.precio_total += precio_pos #Actualizo el precio total
                pedido.seña = pedido.precio_total/2 #Actualizo la seña
                detalle.tiempo_prod_lote = detalle.cantidad * prenda.tiempo_prod_prenda #Calculo el tiempo de produccion por lote

            #Asocio datos de prenda y pedido a detalle
            detalle.prenda = prenda
            detalle.pedido = pedido

            pedido.save() # Actualizo el pedido
            detalle.save() # Actualizo el detalle
            id_detalle = detalle.id_detalle #Obtengo el id del detalle
            return redirect('/pedido/volver_pedido/'+str(id_pedido))
    ingredientes = Ingrediente.objects.filter(prenda_id = id_prenda)
    return render(request,'prenda/editar_prenda.html',{'prenda_form':prenda_form,'detalle_form':detalle_form, 'pedido':pedido, 'prenda':prenda, 'ingredientes':ingredientes, 'detalle':detalle})

#Listar todos las ingredientes
def ListarIngrediente (request):
    ingredientes = Ingrediente.objects.all()
    return redirect('index')
#Editar un ingrediente
def EditarIngrediente (request,id_ingrediente, id_pedido, id_detalle, id_prenda):
    try:
        error = None
        ingrediente_form=None
        ingrediente = Ingrediente.objects.get(id_ingrediente=id_ingrediente)
        if request.method=='GET':
            ingrediente_form=ingredienteForm(instance=ingrediente)
        else:
            ingrediente_form=IngredienteForm(request.POST, instance=ingrediente)
            if ingrediente_form.is_valid():
                ingrediente_form.save()
            return redirect('/prenda/editar_material/'+str(ingrediente.id_ingrediente),{'ingrediente_form':ingrediente_form})
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_ingrediente.html',{'ingrediente_form':ingrediente_form, 'error':error})
#Eliminar un ingrediente
def EliminarIngrediente (request,id_ingrediente, id_pedido, id_detalle, id_prenda):
    ingrediente = Ingrediente.objects.get(id_ingrediente=id_ingrediente)
    detalle = Detalle.objects.get(id_detalle = id_detalle)
    material = Material.objects.get(id_material = str(ingrediente.material.id_material))
    cantidad_material = ingrediente.cantidad * detalle.cantidad
    material.stock += cantidad_material
    material.save()
    ingrediente.delete()
    return redirect('/prenda/asignar_material/'+str(id_prenda)+'/'+str(id_detalle)+'/'+str(id_pedido))

#Mostrar unidad de medida al asignar material
def MostrarUnidad(request):
    mt = request.GET.get('material',None)
    material = Material.objects.get(id_material = mt)
    unidad = material.tipo_material.unidad_medida.nombre
    result = {
        'medida': unidad
    }
    print(result)
    return JsonResponse(result)

#Proponer tiempo de produccion estimado
def TiempoProdPrenda(request):
    tp = request.GET.get('tipo_prenda',None)
    if tp!= None:
        pass
    cant_pre = Prenda.objects.filter(tipo_prenda = tp).count()
    prendas = Prenda.objects.filter(tipo_prenda = tp)
    suma = sum(p.tiempo_prod_prenda for p in prendas)
    promedio = 0
    if cant_pre != 0:
        promedio = suma/cant_pre
    result = {
        'promedio': int(promedio)
    }
    return JsonResponse(result)
