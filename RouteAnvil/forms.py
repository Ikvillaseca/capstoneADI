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

        
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise forms.ValidationError("El RUT debe tener el siguiente formato (ejemplo: 12345678-9).")
        return rut
    

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
    
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not re.match(r'^\+?1?\d{9,15}$', telefono):
            raise forms.ValidationError("El numero de telefono debe tener entre 9 y 15 digitos y puede incluir el codigo de pais.")
        return telefono
    
    def clean_empresa_trabajo(self):
        empresa_trabajo = self.cleaned_data['empresa_trabajo']
        if len(empresa_trabajo) < 3:
            raise forms.ValidationError("El nombre de la empresa debe tener al menos 3 caracteres.")
        return empresa_trabajo



#Formulario para poder crear un vehiculo de forma simple con los datos que definimos en el modelo
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculo', 'patente', 'marca', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']
    
    