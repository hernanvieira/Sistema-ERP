from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import ComponenteForm, Tipo_prendaForm, PrendaForm, IngredienteForm, DetalleForm
from .models import Componente, Tipo_prenda, Prenda, Ingrediente
from apps.pedido.models import Pedido, Detalle
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
#Crear un componente
def CrearComponente (request):
    if request.method == 'POST':
        componente_form = ComponenteForm(request.POST)
        if componente_form.is_valid():
            componente = componente_form.save()
            return ListarComponente(request)
        else:
            messages.error(request, 'Ocurrió un error al tratar de crear el componente')
    else:
        componente_form = ComponenteForm()
    return render(request, 'prenda/crear_componente.html',{'componente_form':componente_form})
#Listar todos los componentes
def ListarComponente (request):
    componentes = Componente.objects.all()
    return render(request,'prenda/listar_componente.html',{'componentes':componentes})
#Editar un componente
def EditarComponente (request,id_componente):
    try:
        error = None
        componente_form=None
        componente = Componente.objects.get(id_componente=id_componente)
        if request.method=='GET':
            componente_form=ComponenteForm(instance=componente)
        else:
            componente_form=ComponenteForm(request.POST, instance=componente)
            if componente_form.is_valid():
                componente_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/crear_componente.html',{'componente_form':componente_form, 'error':error})
#Eliminar un componente
def EliminarComponente (request,id_componente):
    error = None
    componente = get_object_or_404(Componente, id_componente=id_componente)
    try:
        if request.method=='POST':
            componente.delete()
            return redirect('prenda:listar_componente')
    except Exception as e:
        error = e
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/eliminar_componente.html',{'componente':componente, 'error':error})

#Crear un tipo de prenda
def CrearTipo_prenda (request):
    if request.method == 'POST':
        tipo_prenda_form = Tipo_prendaForm(request.POST)
        print(tipo_prenda_form.errors)
        if tipo_prenda_form.is_valid():
            tipo_prenda_form.save()
            return ListarTipo_prenda(request)
    else:
        tipo_prenda_form = Tipo_prendaForm()
    return render(request, 'prenda/crear_tipo_prenda.html',{'tipo_prenda_form':tipo_prenda_form})
#Listar todos los tipos de prendas
def ListarTipo_prenda (request):
    tipo_prendas = Tipo_prenda.objects.all()
    return render(request,'prenda/listar_tipo_prenda.html',{'tipo_prendas':tipo_prendas})
#Editar un tipo de prenda
def EditarTipo_prenda (request,id_tipo_prenda):
    try:
        error = None
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
    return render(request,'prenda/crear_tipo_prenda.html',{'tipo_prenda_form':tipo_prenda_form, 'error':error})
#Ver tipo de prenda
def VerTipo_prenda (request,id_tipo_prenda):
    try:
        error = None
        tipo_prenda_form=None
        tipo_prenda = Tipo_prenda.objects.get(id_tipo_prenda=id_tipo_prenda)
        componentes = tipo_prenda.componente.all()
        if request.method=='GET':
            tipo_prenda_form=Tipo_prendaForm(instance=tipo_prenda)
        else:
            tipo_prenda_form=Tipo_prendaForm(request.POST, instance=tipo_prenda)
            if tipo_prenda_form.is_valid():
                tipo_prenda_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/ver_tipo_prenda.html',{'tipo_prenda_form':tipo_prenda_form, 'componentes':componentes, 'error':error})
#Eliminar un tipo de prenda
def EliminarTipo_prenda (request,id_tipo_prenda):
    error = None
    tipo_prenda = get_object_or_404(Tipo_prenda, id_tipo_prenda=id_tipo_prenda)
    try:
        if request.method=='POST':
            tipo_prenda.delete()
            return redirect('prenda:listar_tipo_prenda')
    except Exception as e:
        error = e
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/eliminar_tipo_prenda.html',{'tipo_prenda':tipo_prenda, 'error':error})

#Registrar una prenda al detalle
def CrearPrenda (request,id_pedido):
    if request.method == 'POST':
        prenda_form = PrendaForm(request.POST)
        detalle_form = DetalleForm(request.POST)
        pedido = Pedido.objects.get(id_pedido = id_pedido) #obtendo el pedido
        print(prenda_form.errors)
        print('IMPRIME ALGO?')
        print(request.FILES.get('txtImagen'))
        if prenda_form.is_valid() and detalle_form.is_valid():
            prenda = prenda_form.save(commit = False) #Guardo prenda
            prenda.imagen = request.FILES.get('txtImagen')
            prenda.save()
            detalle = detalle_form.save() #Guardo detalle
            if 'boton_asignar_material' in request.POST:
                prenda_form=PrendaForm(request.POST, instance=prenda)
                if prenda_form.is_valid():
                    prenda_form.save()
                ingrediente_form = IngredienteForm()
                return redirect('/prenda/asignar_material/'+str(prenda.id_prenda)+'/'+str(detalle.id_detalle)+'/'+str(pedido.id_pedido),{'ingrediente_form':ingrediente_form})
            detalle.tiempo_prod_lote = detalle.cantidad * prenda.tiempo_prod_prenda #Calculo el tiempo de produccion por lote
            detalle.save() #Actualizo el detalle
            pedido.precio_total += prenda.precio * detalle.cantidad #Calculo precio total
            pedido.seña = pedido.precio_total/2
            # Asocio datos de prenda y pedido a detalle
            detalle.prenda = prenda
            detalle.pedido = pedido
            pedido.save() # Actualizo el pedido
            detalle.save() # Actualizo el detalle
            id_detalle = detalle.id_detalle #Obtengo el id del detalle
            return redirect('/pedido/volver_pedido/'+str(id_pedido))
        else:
            messages.error(request, 'Ocurrió un error al tratar de agregar una prenda')
    else:
        prenda_form = PrendaForm()
        detalle_form = DetalleForm()
        pedido = Pedido.objects.get(id_pedido = id_pedido) #obtendo el pedido
    return render(request, 'prenda/crear_prenda.html',{'prenda_form':prenda_form,'detalle_form':detalle_form,'pedido':pedido})
#Listar todos las prendas
def ListarPrenda (request):
    prendas = Prenda.objects.all()
    return redirect('index')
#Editar una prenda
def EditarPrenda (request,id_prenda,id_detalle,id_pedido):
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
    if request.method == 'POST':
        ingrediente_form = IngredienteForm(request.POST)
        prenda = Prenda.objects.get(id_prenda=id_prenda)
        detalle = Detalle.objects.get(id_detalle=id_detalle)
        if ingrediente_form.is_valid():
            ingrediente = ingrediente_form.save() #guardo el ingrediente
            print(ingrediente.material.stock)
            detalle.prenda = prenda
            detalle.pedido = pedido
            detalle.save()
            ingrediente.prenda = prenda
            ingrediente.save()
            return redirect('/prenda/volver_prenda/'+str(id_pedido)+'/'+str(id_detalle)+'/'+str(id_prenda))
    else:
        print("WEKELEKE")
        ingrediente_form = IngredienteForm()
    print("ACA SIP")
    return render(request,'prenda/asignar_material.html',{'ingrediente_form':ingrediente_form,'prenda':prenda,'pedido':pedido,})

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
    return render(request,'prenda/crear_prenda.html',{'prenda_form':prenda_form,'detalle_form':detalle_form, 'pedido':pedido, 'prenda':prenda, 'ingredientes':ingredientes})

#Listar todos las ingredientes
def ListarIngrediente (request):
    ingredientes = Ingrediente.objects.all()
    return redirect('index')
#Editar un ingrediente
def EditarIngrediente (request,id_ingrediente):
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
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_ingrediente.html',{'ingrediente_form':ingrediente_form, 'error':error})
#Eliminar un ingrediente
def EliminarIngrediente (request,id_ingrediente):
    ingrediente = Ingrediente.objects.get(id_ingrediente=id_ingrediente)
    if request.method=='POST':
        ingrediente.delete()
        return redirect('material:listar_ingrediente')
    return redirect('index')
