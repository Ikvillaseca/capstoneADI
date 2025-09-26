from django import forms
from .models import Chofer, Pasajero, Vehiculo
import re


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
    
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise forms.ValidationError("El RUT debe tener el siguiente formato (ejemplo: 12345678-9).")
        return rut
    

    def clean_tipo_licencia(self):
        tipo_licencia = self.cleaned_data['tipo_licencia']
        tipos_validos = ['A', 'B', 'C', 'D', 'E']
        if tipo_licencia not in tipos_validos:
            raise forms.ValidationError("El tipo de licencia debe ser uno de los siguientes: A, B, C, D, E.")
        return tipo_licencia


    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if not nombre.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre


    def clean_apellido(self):
        apellido = self.cleaned_data['apellido']
        if not apellido.isalpha():
            raise forms.ValidationError("El apellido solo debe contener letras.")
        return apellido


    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if len(direccion) < 5:
            raise forms.ValidationError("La direccion debe tener al menos 5 caracteres.")
        return direccion


    def clean(self):
        cleaned_data = super().clean()
        fecha_ultimo = cleaned_data.get('fecha_ultimo_control')
        fecha_proximo = cleaned_data.get('fecha_proximo_control')
        if fecha_ultimo and fecha_proximo:
            if fecha_proximo <= fecha_ultimo:
                raise forms.ValidationError("La fecha del proximo control debe ser posterior a la del ultimo control.")
        return cleaned_data



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

    revision_tecnica = forms.DateField(
        input_formats=['%d-%m-%Y'], 
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA'})
    )
    proxima_revision = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA'})
    )

    def clean_patente(self):
        patente = self.cleaned_data['patente']
        if not re.match(r'^([A-Z]{2}\d{4})|([A-Z]{4}\d{2})$', patente):
            raise forms.ValidationError("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12).")
        return patente
    
    def clean_marca(self):
        marca = self.cleaned_data['marca']
        if not marca.isalpha():
            raise forms.ValidationError("La marca solo debe contener letras.")
        return marca
    
    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser un numero positivo.")
        return capacidad
    
    def clean(self):
        cleaned_data = super().clean()
        revision = cleaned_data.get('revision_tecnica')
        proxima_revision = cleaned_data.get('proxima_revision')
        if revision and proxima_revision:
            if proxima_revision <= revision:
                raise forms.ValidationError("La fecha de la proxima revision debe ser posterior a la de la revision tecnica.")
        return cleaned_data