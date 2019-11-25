from django.contrib.auth.forms import AuthenticationForm

class FormularioLogin(AuthenticationForm):
     def __init__(self, *args, **kwargs):
       super(FormularioLogin, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['username'].widget.attrs['placeholder'] = 'Usuario'

       self.fields['password'].widget.attrs['class'] = 'au-input au-input--full'
       self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
