from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .forms import FormularioLogin, UserCreationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import customuser, Rol

#from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def SignUp(request):
    usuarios = customuser.objects.filter(is_active = True)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        errores = form.errors.values() #Obtengo los valores devueltos en el diccionario
        errores = list(errores) #Los casteo a lista porque no es iterable
        for error in errores:
            error = str(error) #Casteo el error a str (solo para eliminar el PUNTITO del <li>)
            error = error.replace('<ul class="errorlist"><li>', '') #Borro la parte esta jaja
            error = error.replace('</li></ul>', '') # y la parte esta jiji
            messages.error(request,error) # PAAAaaaaa un mensajito de error to lindo

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            messages.success(request, 'El usuario se agregó correctamente')
            return redirect('/accounts/signup/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form, 'usuarios':usuarios})

class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    def dispatch(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            print("hay usuario logueado?")
            return HttpResponseRedirect(self.get_success_url())
        else:
            print("No hay usuario logueado")
            return super(Login, self).dispatch(request,*args,**kwargs)
    def form_valid(self, form):
        dj_login(self.request,form.get_user())
        return super(Login, self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

def VerPerfil(request):
    usuario = request.user #Obtengo el usuario registrado actualmente
    form = UserCreationForm(instance = usuario)
    return render(request, 'usuario/ver_perfil.html',{'form':form})

def EditarPerfil(request,id):
    usuario = customuser.objects.get(id = id) #Obtengo el usuario registrado actualmente
    form = UserCreationForm(instance = usuario)
    if request.method == 'POST':
            usernam = request.user.username
            username = request.POST.get('username', None)
            email = request.POST.get('email', None)
            rol = request.POST.get('rol', None)
            if rol != None:
                rol = Rol.objects.get(id_rol = rol)
            nuevapass1 = request.POST.get('password1', None)
            nuevapass2 = request.POST.get('password2', None)

            if nuevapass1 == nuevapass2 and nuevapass1 != None:
                # A backend authenticated the credentials
                u = customuser.objects.get(id=id)
                u.username = username
                u.email = email
                if rol != None:
                    u.rol = rol
                u.set_password(nuevapass1)
                u.save()
                messages.success(request, "Se actualizó correctamente el usuario")
                return redirect ('/usuario/editar_perfil/'+str(id))
            else:
                messages.error(request, "No se pudo actualizar el usuario")
                # No backend authenticated the credentials
    return render(request, 'usuario/editar_perfil.html',{'form':form})

def EliminarUsuario(request,id):
    usuario = customuser.objects.get(id=id)
    usuario.is_active = False
    usuario.save()

    messages.error(request,'Se dió de baja el usuario' + usuario.username)
    return redirect('/accounts/signup/')
