from django import forms
from .models import Usuario


class RegistroUsuario(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = [
            'nombre',
            'contraseña',
            'email',
        ]
        labels = {
            'nickname': 'Nombre de usuario',
            'contraseña': 'Contraseña',
            'email': 'Email',
        }
