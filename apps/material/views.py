from django.shortcuts import render, redirect
from tp_final.forms import Tipo_materialForm
from .models import Tipo_material
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
    return render(request, 'tipo_material/crear_tipo_material.html',{'tipo_material_form':tipo_material_form})
#Listar todos los tipo_materiales
def ListarTipo_material (request):
    tipo_materiales = tipo_material.objects.all()
    return render(request,'tipo_material/listar_tipo_material.html',{'tipo_materiales':tipo_materiales})
#Editar un tipo_material
def EditarTipo_material (request,id_tipo_material):
    try:
        error = None
        tipo_material_form=None
        tipo_material = tipo_material.objects.get(id_tipo_material=id_tipo_material)
        if request.method=='GET':
            tipo_material_form=Tipo_materialForm(instance=tipo_material)
        else:
            tipo_material_form=Tipo_materialForm(request.POST, instance=tipo_material)
            if tipo_material_form.is_valid():
                tipo_material_form.save()
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'tipo_material/crear_tipo_material.html',{'tipo_material_form':tipo_material_form, 'error':error})
#Eliminar un tipo_material
def EliminarTipo_material (request,id_tipo_material):
    tipo_material = tipo_material.objects.get(id_tipo_material=id_tipo_material)
    if request.method=='POST':
        tipo_material.delete()
        return redirect('tipo_material:listar_tipo_material')
    return render(request,'tipo_material/eliminar_tipo_material.html',{'tipo_material':tipo_material})
