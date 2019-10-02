from django.shortcuts import render, redirect, get_object_or_404
from tp_final.forms import Tipo_materialForm, MaterialForm, Unidad_medidaForm, CompraForm
from .models import Tipo_material, Material, Unidad_medida, Compra
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

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

#Eliminar un cliente
def EliminarTipo_material (request,id_tipo_material):
    tipo_material = get_object_or_404(Tipo_material,id_tipo_material=id_tipo_material)
    try:
        tipo_material.delete()
        tipo_materiales = Tipo_material.objects.all()
        return render (request,'material/listar_tipo_material',{'tipo_material':tipo_material,'tipo_materiales':tipo_materiales})
    except Exception as e:
        messages.error(request, 'Ocurrió un error al tratar de eliminar el tipo de material')
        tipo_materiales = Tipo_material.objects.all()
        return render(request,'material/listar_tipo_material.html',{'tipo_material':tipo_material,'tipo_materiales':tipo_materiales})

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
    error = None
    try:
        material = None
        material = get_object_or_404(Material,id_material=id_material)
        if request.method=='POST':
            material.delete()
            return redirect('material:listar_material')
    except Exception as e:
        error = e
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/eliminar_material.html',{'material':material, 'error':error})

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
    error = None
    try:
        unidad_medida = get_object_or_404(Unidad_medida,id_unidad=id_unidad)
        if request.method=='POST':
            unidad_medida.delete()
            return redirect('material:listar_unidad_medida')
    except Exception as e:
        error = e
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'material/eliminar_unidad_medida.html',{'unidad_medida':unidad_medida, 'error':error})

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
