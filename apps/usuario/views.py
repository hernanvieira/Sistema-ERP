from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .forms import FormularioLogin
from django.contrib.auth import login as dj_login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

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
    return render(request, 'usuario/ver_perfil.html')
