from django import forms
from .models import Chofer, Pasajero, Vehiculo
from .choices import estado, tipo_licencia  # Agregar el import
import re


#Formulario para poder crear un chofer
class FormularioChofer(forms.ModelForm):
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
        fields = ['rut', 'nombre', 'apellido', 'tipo_licencia', 'direccion', 'fecha_ultimo_control', 'fecha_proximo_control']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_licencia': forms.Select(choices=tipo_licencia, attrs={'class': 'form-select'}),  # Usar las choices
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise forms.ValidationError("El RUT debe tener el siguiente formato (ejemplo: 12345678-9).")
        
        if not self.instance.pk and Chofer.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Ya existe un chofer con este RUT.")
        
        return rut
    
    def clean_tipo_licencia(self):
        tipo_licencia = self.cleaned_data['tipo_licencia']
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
        rut = self.cleaned_data['rut']
        if not re.match(r'^\d{7,8}-[\dkK]$', rut):
            raise forms.ValidationError("El RUT debe tener el siguiente formato (ejemplo: 12345678-9).")
        
        if not self.instance.pk and Pasajero.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Ya existe un pasajero con este RUT.")
        
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


# Formulario para crear vehículos
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['id_vehiculo', 'patente', 'marca', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']
        widgets = {
            'id_vehiculo': forms.NumberInput(attrs={'class': 'form-control'}),
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
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
        patente = self.cleaned_data['patente']
        if not re.match(r'^([A-Z]{2}\d{4})|([A-Z]{4}\d{2})$', patente):
            raise forms.ValidationError("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12).")
        
        if not self.instance.pk and Vehiculo.objects.filter(patente=patente).exists():
            raise forms.ValidationError("Ya existe un vehículo con esta patente.")
        
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


# Formulario específico para modificar vehículos
class VehiculoModificarForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'capacidad', 'estado', 'revision_tecnica', 'proxima_revision']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
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

# Formulario específico para modificar pasajeros
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

#Formulario específico para modificar choferes
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
        fields = ['nombre', 'apellido', 'tipo_licencia', 'direccion', 'fecha_ultimo_control', 'fecha_proximo_control']  # Sin RUT
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_licencia': forms.Select(choices=tipo_licencia, attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
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