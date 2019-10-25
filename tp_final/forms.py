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
    def clean_apellido(self):
        value = self.cleaned_data.get('apellido')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value
    # def clean_nombre(self):
    #     value = self.cleaned_data.get('nombre')
    #     if not value.isalpha() :
    #         raise forms.ValidationError("No puede introducir numeros")
    #     return value
    #Evito que cambie el DNI al editar el cliente
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
        fields = ['nombre','descripcion','tipo' ]
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value
    def clean_descripcion(self):
        value = self.cleaned_data.get('descripcion')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value

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
        fields = ['nombre','color','tipo_material','stock']
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
        'material' : forms.Select(attrs={'class' : 'js-example-basic-single'}),
        }

class PedidoForm (forms.ModelForm):
    class Meta:
        CHOICES= [
        ('2', 'Alta'),
        ('1', 'Media'),
        ('0', 'Baja'),
        ]
        model = Pedido
        fields = ['fecha_entrega', 'precio_total', 'entrega', 'seña', 'prioridad_entrega','cliente']
        widgets = {
        'fecha_entrega' : forms.DateInput(),
        'prioridad_entrega' : forms.Select(choices = CHOICES),
        'cliente' : forms.Select(attrs={'class' : 'js-example-basic-single'})
        }
    # #Evito que cambie el Cliente al editar el Pedido
    # def __init__(self, *args, **kwargs):
    #     super(PedidoForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.cliente:
    #         self.fields['cliente'].widget = forms.HiddenInput()
    #
    # def clean_cliente(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.cliente:
    #         return instance.cliente
    #     else:
    #         return self.cleaned_data['cliente']

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['cantidad', 'tiempo_prod_lote', 'pedido','prenda']

class ComponenteForm (forms.ModelForm):
    class Meta:
        model = Componente
        fields = ['nombre']
    # def clean_nombre(self):
    #     nombre = self.cleaned_data.get('nombre')
    #     if not nombre.isalpha():
    #         raise forms.ValidationError("No puede introducir numeros")
    #     return nombre

class Tipo_prendaForm (forms.ModelForm):
    class Meta:
        model = Tipo_prenda
        fields = ['nombre','componente']
        widgets = {
        'componente' : forms.SelectMultiple(attrs={'class' : 'js-example-basic-multiple', 'multiple':'multiple'}),
        }
    def clean_nombre(self):
        value = self.cleaned_data.get('nombre')
        if not value.isalpha():
            raise forms.ValidationError("No puede introducir numeros")
        return value


class PrendaForm (forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['talle', 'tiempo_prod_prenda','tipo_prenda','precio','imagen']

class IngredienteForm (forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['cantidad', 'prenda', 'material']
        widgets = {
        # 'componente' : forms.Select(attrs={'class' : 'js-example-basic-single'}),
        'material' : forms.Select(attrs={'class' : 'js-example-basic-single'}),
        }
