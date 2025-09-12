from django import forms
from .models import Chofer, Pasajero


#Formulario para poder crear un chofer de forma simple con los datos que definimos en el modelo
class FormularioChofer(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = ['rut', 'nombre', 'apellido', 'tipo_licencia', 'direccion', 'fecha_ultimo_control', 'fecha_proximo_control']



#Formulario para poder crear un pasajero de forma simple con los datos que definimos en el modelo
class FormularioPasajero(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'empresa_trabajo']