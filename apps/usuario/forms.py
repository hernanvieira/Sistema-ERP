from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import customuser

class FormularioLogin(AuthenticationForm):
     def __init__(self, *args, **kwargs):
       super(FormularioLogin, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['username'].widget.attrs['placeholder'] = 'Usuario'

       self.fields['password'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class UserCreationForm(UserCreationForm):
    class Meta:
        model = customuser
        fields = ('username', 'rol', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
       super(UserCreationForm, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['username'].widget.attrs['placeholder'] = 'Usuario'

       self.fields['password1'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'

       self.fields['password2'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password2'].widget.attrs['placeholder'] = 'Contraseña'

       self.fields['rol'].widget.attrs['class'] = 'js-example-basic-single'
