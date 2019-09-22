from django.shortcuts import render, redirect
from tp_final.forms import Tipo_materialForm, MaterialForm
from .models import Tipo_material, Material
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
