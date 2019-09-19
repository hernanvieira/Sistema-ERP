from django.shortcuts import render, redirect
from tp_final.forms import ComponenteForm, Tipo_prendaForm
from .models import Componente, Tipo_prenda
from django.core.exceptions import ObjectDoesNotExist
#Crear un componente
def CrearComponente (request):
    if request.method == 'POST':
        componente_form = ComponenteForm(request.POST)
        if componente_form.is_valid():
            componente_form.save()
            return ListarComponente(request)
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
    componente = Componente.objects.get(id_componente=id_componente)
    if request.method=='POST':
        componente.delete()
        return redirect('prenda:listar_componente')
    return render(request,'prenda/eliminar_componente.html',{'componente':componente})

#Crear un tipo de prenda
def CrearTipo_prenda (request):
    if request.method == 'POST':
        tipo_prenda_form = Tipo_prendaForm(request.POST)
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
            return redirect('index')
    except ObjectDoesNotExist as e:
        error = e
    return render(request,'prenda/crear_tipo_prenda.html',{'tipo_prenda_form':tipo_prenda_form, 'error':error})
#Eliminar un tipo de prenda
def EliminarTipo_prenda (request,id_tipo_prenda):
    tipo_prenda = Tipo_prenda.objects.get(id_tipo_prenda=id_tipo_prenda)
    if request.method=='POST':
        tipo_prenda.delete()
        return redirect('prenda:listar_tipo_prenda')
    return render(request,'prenda/eliminar_tipo_prenda.html',{'tipo_prenda':tipo_prenda})
