from django import forms
from .models import Chofer, Pasajero, Vehiculo
from .choices import estado, tipo_licencia
from .validadores import (
    validar_rut, validar_texto, validar_telefono, 
    validar_empresa, validar_direccion, validar_fechas_control_medico,
    validar_patente, validar_capacidad, validar_fechas_revision_tecnica
)  # Importar los validadores
import re

#Formulario para poder crear un chofer
class FormularioChofer(forms.ModelForm):
    class Meta:
        model = Chofer
        fields = ['rut', 'nombre', 'apellido', 'tipo_licencia', 'direccion', 
                 'fecha_ultimo_control', 'fecha_proximo_control', 'id_vehiculo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 12345678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_licencia': forms.Select(attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ultimo_control': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_proximo_control': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'id_vehiculo': forms.Select(attrs={'class': 'form-select'}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer el vehículo opcional
        self.fields['id_vehiculo'].required = False
        self.fields['id_vehiculo'].empty_label = "Sin vehículo asignado"
        
        #Solo mostrar vehículos disponibles
        self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(estado='A')

    def clean_rut(self):
        return validar_rut(self.cleaned_data['rut'], Chofer, self.instance)
    
    def clean_nombre(self):
        return validar_texto(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_texto(self.cleaned_data['apellido'])

    def clean_direccion(self):
        return validar_direccion(self.cleaned_data['direccion'])

    def clean(self):
        cleaned_data = super().clean()
        fecha_ultimo = cleaned_data.get('fecha_ultimo_control')
        fecha_proximo = cleaned_data.get('fecha_proximo_control')
        validar_fechas_control_medico(fecha_ultimo, fecha_proximo)
        return cleaned_data

# Formulario para modificar choferes
class FormularioChoferModificar(forms.ModelForm):
    fecha_ultimo_control = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )
    fecha_proximo_control = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )

    class Meta:
        model = Chofer
        fields = ['nombre', 'apellido', 'tipo_licencia', 'direccion', 'fecha_ultimo_control', 'fecha_proximo_control', 'id_vehiculo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_licencia': forms.Select(choices=tipo_licencia, attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'id_vehiculo': forms.Select(attrs={'class': 'form-select'}),  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['id_vehiculo'].required = False
        self.fields['id_vehiculo'].empty_label = "Sin vehículo asignado"
        
        self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(estado='A')
    
    def clean_nombre(self):
        return validar_texto(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_texto(self.cleaned_data['apellido'])

    def clean_direccion(self):
        return validar_direccion(self.cleaned_data['direccion'])

    def clean(self):
        cleaned_data = super().clean()
        fecha_ultimo = cleaned_data.get('fecha_ultimo_control')
        fecha_proximo = cleaned_data.get('fecha_proximo_control')
        validar_fechas_control_medico(fecha_ultimo, fecha_proximo)
        return cleaned_data

#Formulario para poder crear un pasajero
class FormularioPasajero(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'empresa_trabajo']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean_rut(self):
        return validar_rut(self.cleaned_data['rut'], Pasajero, self.instance)
    
    def clean_nombre(self):
        return validar_texto(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_texto(self.cleaned_data['apellido'])
    
    def clean_telefono(self):
        return validar_telefono(self.cleaned_data['telefono'])
    
    def clean_empresa_trabajo(self):
        return validar_empresa(self.cleaned_data['empresa_trabajo'])

# Formulario para modificar pasajeros 
class FormularioPasajeroModificar(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'apellido', 'telefono', 'empresa_trabajo']  # Sin RUT
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_nombre(self):
        return validar_texto(self.cleaned_data['nombre'])

    def clean_apellido(self):
        return validar_texto(self.cleaned_data['apellido'])
    
    def clean_telefono(self):
        return validar_telefono(self.cleaned_data['telefono'])
    
    def clean_empresa_trabajo(self):
        return validar_empresa(self.cleaned_data['empresa_trabajo'])

# Formularios de vehículos
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'anio', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=estado, attrs={'class': 'form-select'}),
            'revision_tecnica': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-AAAA'}),
            'proxima_revision': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-AAAA'}),
        }

    revision_tecnica = forms.DateField(
        input_formats=['%d-%m-%Y'], 
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )
    proxima_revision = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )

    def clean_patente(self):
        return validar_patente(self.cleaned_data['patente'], self.instance)
    
    def clean_marca(self):
        return validar_texto(self.cleaned_data['marca'])
    
    def clean_capacidad(self):
        return validar_capacidad(self.cleaned_data['capacidad'])
    
    def clean(self):
        cleaned_data = super().clean()
        revision = cleaned_data.get('revision_tecnica')
        proxima_revision = cleaned_data.get('proxima_revision')
        validar_fechas_revision_tecnica(revision, proxima_revision)
        return cleaned_data

class VehiculoModificarForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(choices=estado, attrs={'class': 'form-select'}),
            'revision_tecnica': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-AAAA'}),
            'proxima_revision': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-AAAA'}),
        }

    revision_tecnica = forms.DateField(
        input_formats=['%d-%m-%Y'], 
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )
    proxima_revision = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'DD-MM-AAAA', 'class': 'form-control'})
    )
    
    def clean_marca(self):
        return validar_texto(self.cleaned_data['marca'])
    def clean_capacidad(self):
        return validar_capacidad(self.cleaned_data['capacidad'])
    
    def clean(self):
        cleaned_data = super().clean()
        revision = cleaned_data.get('revision_tecnica')
        proxima_revision = cleaned_data.get('proxima_revision')
        validar_fechas_revision_tecnica(revision, proxima_revision)
        return cleaned_data
    
class FormularioViajeSeleccionarPasajeros(forms.Form):
    choices = forms.ModelMultipleChoiceField(
        queryset = Pasajero.objects.all().order_by('empresa_trabajo','apellido','nombre'),
        widget  = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
