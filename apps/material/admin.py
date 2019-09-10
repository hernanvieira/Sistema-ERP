from django.contrib import admin
from .models import Material, Compra, Unidad_medida, Tipo_material
# Register your models here.
admin.site.register(Material)
admin.site.register(Compra)
admin.site.register(Unidad_medida)
admin.site.register(Tipo_material)
