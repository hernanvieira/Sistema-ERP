from django.contrib import admin
from .models import Prenda, Tipo_prenda, Componente, Ingrediente
# Register your models here.
admin.site.register(Prenda)
admin.site.register(Tipo_prenda)
admin.site.register(Componente)
admin.site.register(Ingrediente)
