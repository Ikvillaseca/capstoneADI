import re
from itertools import cycle
from django.core.exceptions import ValidationError
from .models import Chofer, Pasajero, Vehiculo
from datetime import datetime

def _validar_rut_chileno(rut):
    # Limpiar el RUT de puntos y guiones
    rut = rut.upper().replace("-", "").replace(".", "")
    rut_aux = rut[:-1]
    dv = rut[-1:]

    # Validar que el número sea numérico y esté en rango válido
    if not rut_aux.isdigit() or not (1_000_000 <= int(rut_aux) <= 25_000_000):
        return False

    # Calcular dígito verificador
    revertido = map(int, reversed(rut_aux))
    factors = cycle(range(2, 8))
    suma = sum(d * f for d, f in zip(revertido, factors))
    residuo = suma % 11

    # Validar dígito verificador
    if dv == 'K':
        return residuo == 1
    if dv == '0':
        return residuo == 0
    return residuo == 11 - int(dv)



#Funciones que se repiten en los formularios
def validar_rut(rut, modelo, instance=None):
    # Validar formato básico
    if not re.match(r'^\d{7,8}-[\dkK]$', rut):
        raise ValidationError("El RUT debe tener el siguiente formato (ejemplo: 12345678-9).")
    
    # Validar dígito verificador usando el algoritmo chileno
    if not _validar_rut_chileno(rut):
        raise ValidationError("El RUT ingresado no es válido. Verifique el dígito verificador.")
    
    # Validar unicidad
    if not instance or not instance.pk:
        if modelo.objects.filter(rut=rut).exists():
            tipo_modelo = modelo.__name__.lower()
            raise ValidationError(f"Ya existe un {tipo_modelo} con este RUT.")
    
    return rut

def validar_texto(texto):
    if not texto.isalpha():
        raise ValidationError("El texto solo debe contener letras.")
    return texto




#Validaroes de pasajeros

def validar_telefono(telefono):
    #Formato internacional y nacional de celulares chilenos
    if re.match(r'^\+56\d{9}$', telefono):
        return telefono
    if re.match(r'^9\d{8}$', telefono):
        return ('+56'+telefono)
    #Formato internacional cualquier otro pais
    if re.match(r'^\+\d{9,15}$', telefono):
        return telefono
    #Formato invalido
    if not re.match(r'^\+\d{9,15}$', telefono):
        raise ValidationError("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)")

def validar_empresa(empresa):
    if len(empresa) < 3:
        raise ValidationError("El nombre de la empresa debe tener al menos 3 caracteres.")
    if len(empresa) > 45:
        raise ValidationError("El nombre de la empresa no debe exceder los 45 caracteres.")
    return empresa


#Validadores de choferes
def validar_direccion(direccion):
    if len(direccion) < 5:
        raise ValidationError("La dirección debe tener al menos 5 caracteres.")
    return direccion

def validar_fechas_control_medico(fecha_ultimo_control, fecha_proximo_control):
    #Validador de fechas de control médico para choferes
    if fecha_ultimo_control and fecha_proximo_control:
        if fecha_proximo_control <= fecha_ultimo_control:
            raise ValidationError("La fecha del proximo control debe ser posterior a la del ultimo control.")
    return True


#Validadores de vehiculos
def validar_patente(patente, instance=None):
    if re.match(r'^([A-Z]{2}\d{4})$', patente):
        return patente
    if re.match(r'^([A-Z]{4}\d{2})$', patente):
        return patente
    if not re.match(r'^([A-Z]{2}\d{4})|([A-Z]{4}\d{2})$', patente):
            raise ValidationError("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12).")
    
    # Validar unico patente 
    if not instance or not instance.pk:
        if Vehiculo.objects.filter(patente=patente).exists():
            raise ValidationError("Ya existe un vehículo con esta patente.")
    
    return patente

def validar_modelo(modelo: str):
    if not modelo:
        raise ValidationError("El modelo no puede estar vacío.")
    if len(modelo) < 3:
        raise ValidationError("El modelo debe tener al menos 3 caracteres.")
    if len(modelo) > 45:
        raise ValidationError("El modelo no puede exceder los 45 caracteres.")
    return modelo

def validar_anio(anio: int):
    if anio and (anio < 1950 or anio > datetime.now().year):
        raise ValidationError("El año debe estar entre 1950 y el año actual.")
    return anio

def validar_capacidad(capacidad: str):
    try:
        capacidad = float(capacidad)
    except ValueError:
        raise ValidationError("La capacidad debe ser un número positivo.")
    if capacidad != int(capacidad):
        raise ValidationError("La capacidad debe ser un número positivo.")
    if capacidad <= 0:
        raise ValidationError("La capacidad debe ser un número positivo.")
    return capacidad

def validar_fechas_revision_tecnica(revision_tecnica, proxima_revision):
    if revision_tecnica and proxima_revision:
        if proxima_revision <= revision_tecnica:
            raise ValidationError("La fecha de la proxima revision debe ser posterior a la de la revision tecnica.")
    return True

def validar_vehiculo_unico_chofer(vehiculo, chofer_instance=None):
    if vehiculo:
        from .models import Chofer
        # Buscar si hay otro chofer con el mismo vehículo
        choferes_con_vehiculo = Chofer.objects.filter(id_vehiculo=vehiculo)
        
        if chofer_instance and chofer_instance.pk:
            choferes_con_vehiculo = choferes_con_vehiculo.exclude(pk=chofer_instance.pk)
        
        if choferes_con_vehiculo.exists():
            chofer_actual = choferes_con_vehiculo.first()
            raise ValidationError(f'El vehículo {vehiculo.patente} ya está asignado al chofer {chofer_actual.nombre} {chofer_actual.apellido}.')
    
    return vehiculo