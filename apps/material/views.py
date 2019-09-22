from django.shortcuts import render, redirect
from tp_final.forms import Tipo_materialForm, MaterialForm, Unidad_medidaForm
from .models import Tipo_material, Material, Unidad_medida
from django.core.exceptions import ObjectDoesNotExist

#Crear un tipo de tipo_material
def CrearTipo_material (request):
    if request.method == 'POST':
        tipo_material_form = Tipo_materialForm(request.POST)
        if tipo_material_form.is_valid():
            tipo_material_form.save()
            return ListarTipo_material(request)
    else:
        tipo_material_form = Tipo_materialForm()
    return render(request, 'material/crear_tipo_material.html',{'tipo_material_form':tipo_material_form})
#Listar todos los tipo_materiales
def ListarTipo_material (request):
    tipo_materiales = Tipo_material.objects.all()
    return render(request,'material/listar_tipo_material.html',{'tipo_materiales':tipo_materiales})
#Editar un tipo_material
def EditarTipo_material (request,id_tipo_material):
    try:
        error = None
        tipo_material_form=None
        tipo_material = Tipo_material.objects.get(id_tipo_material=id_tipo_material)
        if request.method=='GET':
            tipo_material_form=Tipo_materialForm(instance=tipo_material)
        else:
            tipo_material_form=Tipo_materialForm(request.POST, instance=tipo_material)
            if tipo_material_form.is_valid():
                tipo_material_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_tipo_material.html',{'tipo_material_form':tipo_material_form, 'error':error})
#Eliminar un tipo_material
def EliminarTipo_material (request,id_tipo_material):
    tipo_material = Tipo_material.objects.get(id_tipo_material=id_tipo_material)
    if request.method=='POST':
        tipo_material.delete()
        return redirect('material:listar_tipo_material')
    return render(request,'material/eliminar_tipo_material.html',{'tipo_material':tipo_material})

#Crear un material
def CrearMaterial (request):
    if request.method == 'POST':
        material_form = MaterialForm(request.POST)
        if material_form.is_valid():
            material_form.save()
            return ListarMaterial(request)
    else:
        material_form = MaterialForm()
    return render(request, 'material/crear_material.html',{'material_form':material_form})
#Listar todos los materiales
def ListarMaterial (request):
    materiales = Material.objects.all()
    return render(request,'material/listar_material.html',{'materiales':materiales})
#Editar un material
def EditarMaterial (request,id_material):
    try:
        error = None
        material_form=None
        material = Material.objects.get(id_material=id_material)
        if request.method=='GET':
            material_form=MaterialForm(instance=material)
        else:
            material_form=MaterialForm(request.POST, instance=material)
            if material_form.is_valid():
                material_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_material.html',{'material_form':material_form, 'error':error})
#Eliminar un material
def EliminarMaterial (request,id_material):
    material = Material.objects.get(id_material=id_material)
    if request.method=='POST':
        material.delete()
        return redirect('material:listar_material')
    return render(request,'material/eliminar_material.html',{'material':material})

#Crear una unidad de medida
def CrearUnidad_medida (request):
    if request.method == 'POST':
        unidad_medida_form = Unidad_medidaForm(request.POST)
        if unidad_medida_form.is_valid():
            unidad_medida_form.save()
            return ListarUnidad_medida(request)
    else:
        unidad_medida_form = Unidad_medidaForm()
    return render(request, 'material/crear_unidad_medida.html',{'unidad_medida_form':unidad_medida_form})
#Listar todos las unidad_medidas
def ListarUnidad_medida (request):
    unidad_medidas = Unidad_medida.objects.all()
    return render(request,'material/listar_unidad_medida.html',{'unidad_medidas':unidad_medidas})
#Editar un unidad_medida
def EditarUnidad_medida (request,id_unidad):
    try:
        error = None
        unidad_medida_form=None
        unidad_medida = Unidad_medida.objects.get(id_unidad=id_unidad)
        if request.method=='GET':
            unidad_medida_form=Unidad_medidaForm(instance=unidad_medida)
        else:
            unidad_medida_form=Unidad_medidaForm(request.POST, instance=unidad_medida)
            if unidad_medida_form.is_valid():
                unidad_medida_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/crear_unidad_medida.html',{'unidad_medida_form':unidad_medida_form, 'error':error})
#Eliminar un unidad_medida
def EliminarUnidad_medida (request,id_unidad):
    unidad_medida = Unidad_medida.objects.get(id_unidad=id_unidad)
    if request.method=='POST':
        unidad_medida.delete()
        return redirect('material:listar_unidad_medida')
    return render(request,'material/eliminar_unidad_medida.html',{'unidad_medida':unidad_medida})
