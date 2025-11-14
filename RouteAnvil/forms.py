from django import forms
from django.db.models import Q
from .models import Chofer, Pasajero, Vehiculo, Parada
from .choices import estado, tipo_licencia, parada
from .validadores import (
    validar_rut, validar_texto, validar_telefono, validar_direccion,
    validar_empresa, validar_patente, validar_capacidad, 
    validar_fechas_control_medico, validar_fechas_revision_tecnica,
    validar_vehiculo_unico_chofer
)
from .viajes_direcciones import geocoding_desde_direccion


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
        self.fields['id_vehiculo'].required = False
        self.fields['id_vehiculo'].empty_label = "Sin vehículo asignado"
                
        if self.instance.pk and self.instance.id_vehiculo:
            self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(
                Q(estado='A') & (Q(chofer__isnull=True) | Q(pk=self.instance.id_vehiculo.pk))
            )
        else:
            self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(
                estado='A', chofer__isnull=True
            )

    def clean_id_vehiculo(self):
        vehiculo = self.cleaned_data.get('id_vehiculo')
        if vehiculo:
            return validar_vehiculo_unico_chofer(vehiculo, self.instance)
        return vehiculo

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
                
        if self.instance.pk and self.instance.id_vehiculo:
            self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(
                Q(estado='A') & (Q(chofer__isnull=True) | Q(pk=self.instance.id_vehiculo.pk))
            )
        else:
            self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(
                estado='A', chofer__isnull=True
            )
    
    def clean_id_vehiculo(self):
        vehiculo = self.cleaned_data.get('id_vehiculo')
        if vehiculo:
            return validar_vehiculo_unico_chofer(vehiculo, self.instance)
        return vehiculo

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
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'empresa_trabajo', 'paradero_deseado']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'paradero_deseado': forms.Select(attrs={'class': 'form-select'}),  
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paradero_deseado'].required = False
        self.fields['paradero_deseado'].empty_label = "Sin paradero asignado"
        self.fields['paradero_deseado'].queryset = Parada.objects.all().order_by('nombre')

    def clean(self):
        cleaned_data = super().clean()
        paradero_deseado = cleaned_data.get('paradero_deseado')
        return cleaned_data
    
        
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
        fields = ['nombre', 'apellido', 'telefono', 'empresa_trabajo', 'paradero_deseado'] # Sin RUT
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'paradero_deseado': forms.Select(attrs={'class': 'form-select'}),  

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paradero_deseado'].required = False
        self.fields['paradero_deseado'].empty_label = "Sin paradero asignado"
        self.fields['paradero_deseado'].queryset = Parada.objects.all().order_by('nombre')

    def clean(self):
        cleaned_data = super().clean()
        paradero_deseado = cleaned_data.get('paradero_deseado')
        return cleaned_data
    
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

#Formulario para poder crear un paradero
class FormularioParadero(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['nombre', 'tipo_parada', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre (opcional)'}),
            'tipo_parada': forms.Select(choices=parada, attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].required = False

# Formulario para modificar paraderos 
class FormularioParaderoModificar(forms.ModelForm):
    class Meta:
        model = Parada
        fields = ['nombre', 'tipo_parada', 'direccion', 'latitud', 'longitud']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_parada': forms.Select(choices=parada, attrs={'class': 'form-select'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'latitud': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para seleccionar destino en creación de viajes
class FormularioDestinoViaje(forms.Form):
    tipo_viaje = forms.ChoiceField(
        choices=[
            ('IDA', 'Viaje de Ida - Recoger pasajeros en paraderos y llevarlos a empresa'),
            ('VUELTA', 'Viaje de Vuelta - Recoger pasajeros en empresa y llevarlos a paraderos')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='IDA',
        label='Tipo de viaje'
    )
    
    tipo_seleccion = forms.ChoiceField(
        choices=[
            ('paradero', 'Seleccionar paradero/empresa existente'),
            ('direccion', 'Ingresar dirección personalizada')
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='paradero',
        label='Tipo de selección'
    )
    
    paradero_existente = forms.ModelChoiceField(
        queryset=Parada.objects.all().order_by('nombre'),
        required=False,
        empty_label="Seleccione un paradero o empresa",
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Paradero/Empresa'
    )
    
    direccion_personalizada = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Av. Libertador Bernardo O\'Higgins 1058, Santiago'
        }),
        label='Dirección'
    )
    
    nombre_temporal = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: Oficina Central'
        }),
        label='Nombre del lugar (opcional)'
    )

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_seleccion')
        paradero = cleaned_data.get('paradero_existente')
        direccion = cleaned_data.get('direccion_personalizada')
        
        if tipo == 'paradero' and not paradero:
            raise forms.ValidationError('Debe seleccionar un paradero o empresa')
        
        if tipo == 'direccion' and not direccion:
            raise forms.ValidationError('Debe ingresar una dirección')
        
        return cleaned_data
    
    def get_punto_encuentro(self):
        """Retorna el punto de encuentro (origen o destino según tipo)"""
        
        tipo = self.cleaned_data.get('tipo_seleccion')
        
        if tipo == 'paradero':
            return self.cleaned_data.get('paradero_existente')
        
        # Crear paradero desde dirección
        direccion = self.cleaned_data.get('direccion_personalizada')
        nombre = self.cleaned_data.get('nombre_temporal') or 'Punto de Encuentro'
        
        lat, lon, direccion_formateada, tipo_parada = geocoding_desde_direccion(direccion)
        
        if lat and lon:
            destino = Parada(
                nombre=nombre,
                direccion=direccion_formateada,
                latitud=lat,
                longitud=lon,
                tipo_parada=tipo_parada
            )
            destino.save()
            return destino
        else:
            raise forms.ValidationError('No se pudo geocodificar la dirección')