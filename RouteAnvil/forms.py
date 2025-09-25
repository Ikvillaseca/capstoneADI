from django import forms
from .models import Chofer, Pasajero, Vehiculo


#Formulario para poder crear un chofer de forma simple con los datos que definimos en el modelo
class FormularioChofer(forms.ModelForm):
    fecha_ultimo_control = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA'})
    )
    fecha_proximo_control = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA'})
    )
    class Meta:
        model = Chofer
        fields = ['rut', 'nombre', 'apellido', 'tipo_licencia', 'direccion', 'fecha_ultimo_control', 'fecha_proximo_control']



#Formulario para poder crear un pasajero de forma simple con los datos que definimos en el modelo
class FormularioPasajero(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'empresa_trabajo']

#Formulario para poder crear un vehiculo de forma simple con los datos que definimos en el modelo
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculo', 'patente', 'marca', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']