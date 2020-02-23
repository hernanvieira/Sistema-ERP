from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import customuser

class FormularioLogin(AuthenticationForm):
     def __init__(self, *args, **kwargs):
       super(FormularioLogin, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['username'].widget.attrs['placeholder'] = 'Usuario'

       self.fields['password'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
       self.fields['password'].widget.attrs['id'] = 'myInput'
       self.fields['password'].widget.attrs['style'] = 'width: 89.5%'

class UserCreationForm(UserCreationForm):
    class Meta:
        model = customuser
        fields = ('username', 'rol', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
       super(UserCreationForm, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['username'].widget.attrs['placeholder'] = 'Usuario'

       self.fields['email'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['email'].widget.attrs['placeholder'] = 'Correo@email.com'

       self.fields['password1'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
       self.fields['password1'].widget.attrs['id'] = 'myInput1'
       self.fields['password1'].widget.attrs['style'] = 'width:80%;'

       self.fields['password2'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password2'].widget.attrs['placeholder'] = 'Contraseña'
       self.fields['password2'].widget.attrs['id'] = 'myInput2'
       self.fields['password2'].widget.attrs['style'] = 'width:80%;'

       self.fields['rol'].widget.attrs['class'] = 'js-example-basic-single'
