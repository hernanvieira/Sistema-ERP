from django import forms
from config.models import *
from apps.cliente.models import *
from apps.estado.models import *
from apps.material.models import *
from apps.pedido.models import *
from apps.prenda.models import *

class ClienteForm (forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['dni', 'apellido', 'nombre', 'telefono', 'correo','domicilio']
    def clean_apellido(self):
        value = self.cleaned_data.get('apellido')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['dni'].widget.attrs.update({'readonly': 'True'})

    def clean_dni(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.dni
        else:
            return self.cleaned_data['dni']


class EstadoForm (forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['nombre','descripcion']

class Estado_pedidoForm (forms.ModelForm):
    class Meta:
        model = Estado_pedido
        fields = ['fecha','pedido','estado']

class Estado_loteForm (forms.ModelForm):
    class Meta:
        model = Estado_lote
        fields = ['fecha','pedido','detalle']

class Unidad_medidaForm (forms.ModelForm):
    class Meta:
        model = Unidad_medida
        fields = ['nombre','descripcion']
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value

class Tipo_materialForm (forms.ModelForm):
    class Meta:
        model = Tipo_material
        fields = ['nombre','unidad_medida']
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value

class MaterialForm (forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre','color','tipo_material','stock','stock_minimo']
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value

class CompraForm (forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha','cantidad','material']
        widgets = {
        'fecha' : forms.DateInput(attrs={'type' : 'date', 'id' : 'datePicker'}),
        'material' : forms.Select(attrs={'class' : 'js-example-basic-single', 'id':'combito'}),
        }

class PedidoForm (forms.ModelForm):
    class Meta:
        CHOICES_PRIORIDAD= [
        ('2', 'Alta'),
        ('1', 'Media'),
        ('0', 'Baja'),
        ]
        CHOICES_PUNTAJE= [
        ('0', 'Muy Mala'),
        ('2', 'Mala'),
        ('1', 'Regular'),
        ('1', 'Buena'),
        ('1', 'Muy Buena'),
        ]
        model = Pedido
        fields = ['fecha_entrega', 'precio_total', 'entrega', 'seña', 'prioridad_entrega','cliente']
        widgets = {
        'fecha_entrega' : forms.DateInput(attrs={'type' :'', 'id':'fecha_entrega', 'name':'fecha_entrega'}),
        'prioridad_entrega' : forms.Select(choices = CHOICES_PRIORIDAD),
        'puntaje' : forms.Select(choices = CHOICES_PUNTAJE),
        'cliente' : forms.Select(attrs={'class' : 'js-example-basic-single'})
        }

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['cantidad', 'tiempo_prod_lote', 'pedido','prenda']

class Tipo_prendaForm (forms.ModelForm):
    class Meta:
        model = Tipo_prenda
        fields = ['nombre','medida']
        widgets = {
        'medida' : forms.SelectMultiple(attrs={'class' : 'js-example-basic-multiple', 'multiple':'multiple'}),
        }
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value


class PrendaForm (forms.ModelForm):
    class Meta:
        CHOICES= [
        ('0', 'XS'),
        ('1', 'S'),
        ('2', 'M'),
        ('3', 'L'),
        ('4', 'XL'),
        ('5', 'XXL'),
        ]
        model = Prenda
        fields = ['talle', 'tiempo_prod_prenda','tipo_prenda','precio','imagen']
        widgets = {
        'talle' : forms.Select(choices = CHOICES),
        'tipo_prenda' : forms.Select(attrs={'id':'tipo_prenda', 'name':'tipo_prenda'}),
        'tiempo_prod_prenda' : forms.TextInput(attrs={'id':'tiempo_prod_prenda'})
        }

class IngredienteForm (forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['cantidad', 'prenda', 'material']
        widgets = {
        'material' : forms.Select(attrs={'id':'combito','class' : 'js-example-basic-single'}),
        }

class MedidaForm (forms.ModelForm):
    class Meta:
        model = Medida
        fields = ['nombre_medida', 'unidad_medida']

class Medida_prendaForm (forms.ModelForm):
    class Meta:
        model = Medida_prenda
        fields = ['prenda', 'medida', 'valor']
        widgets = {
        'prenda' : forms.Select(attrs={'class':'form-control'})
        }

class ConfiguracionForm (forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['empresa', 'direccion', 'telefono']

class ConfiguracionMensajeForm (forms.ModelForm):
    class Meta:
        model = ConfiguracionMensaje
        fields = ['en_espera', 'en_produccion', 'cancelado','finalizado','entregado']
