from django.contrib import admin
from .models import Prenda, Tipo_prenda, Medida, Ingrediente
# Register your models here.
admin.site.register(Prenda)
admin.site.register(Tipo_prenda)
admin.site.register(Medida)
admin.site.register(Ingrediente)
