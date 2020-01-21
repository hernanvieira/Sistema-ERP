from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import Tipo_materialForm, MaterialForm, Unidad_medidaForm, CompraForm
from .models import Tipo_material, Material, Unidad_medida, Compra
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from config.models import Configuracion

import json
from django.http import HttpResponse
from django.http import JsonResponse

#Crear un tipo de tipo_material
def CrearTipo_material (request):
    tipo_materiales = Tipo_material.objects.all()
    if request.method == 'POST':
        if 'boton_guardar_listar' in request.POST:
            tipo_material_form = Tipo_materialForm(request.POST)
            if tipo_material_form.is_valid():
                tipo_material_form.save()
                messages.success(request, 'Se creó un tipo de material')
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            return ListarTipo_material(request)
        if 'boton_guardar_agregar' in request.POST:
            tipo_material_form = Tipo_materialForm(request.POST)
            if tipo_material_form.is_valid():
                tipo_material_form.save()
                messages.success(request, 'Se creó un tipo de material')
            else:
                messages.error(request, 'Ocurrió un error al tratar de crear el tipo de material')
            return redirect('/material/crear_tipo_material')
    else:
        tipo_material_form = Tipo_materialForm()
    return render(request, 'material/crear_tipo_material.html',{'tipo_materiales':tipo_materiales,'tipo_material_form':tipo_material_form})
#Listar todos los tipo_materiales
def ListarTipo_material (request):
    tipo_materiales = Tipo_material.objects.all()
    return render(request,'material/listar_tipo_material.html',{'tipo_materiales':tipo_materiales})
#Editar un tipo_material
def EditarTipo_material (request,id_tipo_material):
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
    return render(request,'material/editar_tipo_material.html',{'tipo_materiales':tipo_materiales,'tipo_material_form':tipo_material_form})

#Eliminar un cliente
def EliminarTipo_material (request,id_tipo_material):
    tipo_material = get_object_or_404(Tipo_material,id_tipo_material=id_tipo_material)
    try:
        tipo_material.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el tipo de material')
    tipo_materiales = Tipo_material.objects.all()
    return render(request,'material/listar_tipo_material.html',{'tipo_material':tipo_material,'tipo_materiales':tipo_materiales})

#Crear un material
def CrearMaterial (request):
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
    return render(request, 'material/crear_material.html',{'materiales':materiales,'material_form':material_form})
#Listar todos los materiales
def ListarMaterial (request):
    materiales = Material.objects.all()
    reporte = Configuracion.objects.all().last()
    return render(request,'material/listar_material.html',{'reporte':reporte,'materiales':materiales})
#Editar un material
def EditarMaterial (request,id_material):
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
    return render(request,'material/editar_material.html',{'materiales':materiales,'material_form':material_form, 'error':error})
#Eliminar un material
def EliminarMaterial (request,id_material):
    material = get_object_or_404(Material,id_material=id_material)
    try:
        material.delete()
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el material')
    materiales = Material.objects.all()
    return render(request,'material/listar_material.html',{'materiales':materiales})

#Crear una unidad de medida
def CrearUnidad_medida (request):
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
    return render(request, 'material/crear_unidad_medida.html',{'unidad_medidas':unidad_medidas,'unidad_medida_form':unidad_medida_form})
#Listar todos las unidad_medidas
def ListarUnidad_medida (request):
    unidad_medidas = Unidad_medida.objects.all()
    return render(request,'material/listar_unidad_medida.html',{'unidad_medidas':unidad_medidas})
#Editar un unidad_medida
def EditarUnidad_medida (request,id_unidad):
    unidad_medida = Unidad_medida.objects.get(id_unidad=id_unidad)
    unidad_medidas = Unidad_medida.objects.all()
    if request.method=='GET':
        unidad_medida_form=Unidad_medidaForm(instance=unidad_medida)
    else:
        unidad_medida_form=Unidad_medidaForm(request.POST, instance=unidad_medida)
        if unidad_medida_form.is_valid():
            unidad_medida_form.save()
        return ListarUnidad_medida(request)
    return render(request,'material/editar_unidad_medida.html',{'unidad_medidas':unidad_medidas,'unidad_medida_form':unidad_medida_form})
#Eliminar un unidad_medida
def EliminarUnidad_medida (request,id_unidad):
    try:
        unidad_medida = get_object_or_404(Unidad_medida,id_unidad=id_unidad)
        unidad_medida.delete()
        messages.warning(request, 'Se eliminó la unidad de medida')
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar la unidad de medida')
    return ListarUnidad_medida(request)

#Registrar una compra
def CrearCompra (request):
    if request.method == 'POST':
        compra_form = CompraForm(request.POST)
        if compra_form.is_valid():
            compra_form.save() #Registro la compra
            id_material = request.POST['material'] #Obtengo el id del material involucrado
            cantidad = request.POST['cantidad'] #Obtengo la cantidad de la compra registrada
            material = Material.objects.get(id_material=id_material) #Obtengo el material
            material.stock=material.stock + int(cantidad) #Sumo la cantidad al stock actual
            material.save() #Se actualiza el stock del material

            return ListarMaterial(request)
    else:
        compra_form = CompraForm()
    return render(request, 'material/crear_compra.html',{'compra_form':compra_form})
#Listar todos las compras
def ListarCompra (request):
    compras = Compra.objects.all()
    return render(request,'material/listar_compra.html',{'compras':compras})
#Editar un compra
def EditarCompra (request,id_compra):
    try:
        error = None
        compra_form=None
        compra = Compra.objects.get(id_compra=id_compra)
        if request.method=='GET':
            compra_form=CompraForm(instance=compra)
        else:
            compra_form=CompraForm(request.POST, instance=compra)
            if compra_form.is_valid():
                compra_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_compra.html',{'compra_form':compra_form, 'error':error})
#Eliminar un compra
def EliminarCompra (request,id_compra):
    compra = Compra.objects.get(id_compra=id_compra)
    if request.method=='POST':
        compra.delete()
        return redirect('material:listar_compra')
    return render(request,'material/eliminar_compra.html',{'compra':compra,})

#Mostrar unidad de medida al asignar material
def MostrarUnidad(request):
    mt = request.GET.get('material',None)
    print(mt)
    tipo_material = Tipo_material.objects.get(id_tipo_material = mt)
    print(tipo_material)
    unidad = tipo_material.unidad_medida.nombre
    result = {
        'medida': unidad
    }
    print(result)
    return JsonResponse(result)
