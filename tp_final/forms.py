from django import forms
from apps.cliente.models import *
from apps.estado.models import *
from apps.material.models import *
from apps.pedido.models import *
from apps.prenda.models import *

class ClienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'apellido', 'nombre', 'telefono', 'correo','domicilio']

class EstadoForm (forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['nombre','descripcion','tipo']

class Estado_pedidoForm (forms.ModelForm):
    class Meta:
        model = Estado_pedido
        fields = ['fecha']

class Estado_loteForm (forms.ModelForm):
    class Meta:
        model = Estado_lote
        fields = ['fecha']

class Unidad_medidaForm (forms.ModelForm):
    class Meta:
        model = Unidad_medida
        fields = ['nombre','descripcion']

class Tipo_materialForm (forms.ModelForm):
    class Meta:
        model = Tipo_material
        fields = ['nombre']

class MaterialForm (forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre','color']

class CompraForm (forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha']

class PedidoForm (forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['fecha_entrega', 'precio_total', 'entrega', 'seña', 'prioridad_entrega']

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['cantidad', 'tiempo_prod_lote']

class ComponenteForm (forms.ModelForm):
    class Meta:
        model = Componente
        fields = ['nombre']

class Tipo_prendaForm (forms.ModelForm):
    class Meta:
        model = Tipo_prenda
        fields = ['nombre']

class PrendaForm (forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['talle', 'tiempo_prod_prenda']

class Ingrediente (forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['cantidad', 'prenda', 'componente', 'material']
