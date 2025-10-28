import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Chofer, Pasajero, Vehiculo, Grupo_Pasajeros
from .forms import (VehiculoForm, VehiculoModificarForm, FormularioChofer, 
                   FormularioChoferModificar, FormularioPasajero, FormularioPasajeroModificar, FormularioViajeSeleccionarPasajeros)

# Create your views here.
def index(request):
    return render(request, 'index.html')

# ============ VISTAS CHOFERES ============

#READ
def chofer_lista(request):
    choferes = Chofer.objects.all()
    return render(request, 'choferes/chofer_lista.html', {'choferes': choferes})

#CREATE
def chofer_crear(request):
    if request.method == 'POST':
        form = FormularioChofer(request.POST)
        if form.is_valid():
            chofer = form.save()
            return redirect('chofer_detalle', id_chofer=chofer.id_chofer)
    else:
        form = FormularioChofer()
    return render(request, 'choferes/chofer_crear.html', {'form': form})

#DETAIL (READ ONE)
def chofer_detalle(request, id_chofer):
    chofer = get_object_or_404(Chofer, id_chofer=id_chofer)
    return render(request, 'choferes/chofer_detalle.html', {'chofer': chofer})

#UPDATE
def chofer_modificar(request, id_chofer):
    chofer = get_object_or_404(Chofer, id_chofer=id_chofer)
    if request.method == 'POST':
        form = FormularioChoferModificar(request.POST, instance=chofer)  # Usar nuevo formulario
        if form.is_valid():
            form.save()
            return redirect('chofer_detalle', id_chofer=chofer.id_chofer)
    else:
        form = FormularioChoferModificar(instance=chofer)  # Usar nuevo formulario
    return render(request, 'choferes/chofer_modificar.html', {'form': form, 'chofer': chofer})

#DELETE 
def chofer_eliminar(request, id_chofer):
    chofer = get_object_or_404(Chofer, id_chofer=id_chofer)
    if request.method == 'POST':
        chofer.delete()
        return redirect('chofer_lista')
    return redirect('chofer_lista')

# ============ VISTAS PASAJEROS ============

#READ
def pasajeros_lista(request):
    pasajeros = Pasajero.objects.all()
    return render(request, 'pasajeros/pasajero_lista.html', {'pasajeros': pasajeros})

#CREATE
def pasajero_crear(request):
    if request.method == 'POST':
        form = FormularioPasajero(request.POST)
        if form.is_valid():
            pasajero = form.save()
            return redirect('pasajero_detalles', id_pasajero=pasajero.id_pasajero)
    else:
        form = FormularioPasajero()
    return render(request, 'pasajeros/pasajero_crear.html', {'form': form})

def pasajero_detalles(request, id_pasajero):
    pasajero = get_object_or_404(Pasajero, id_pasajero=id_pasajero)
    return render(request, 'pasajeros/pasajero_detalles.html', {'pasajero': pasajero})

#UPDATE
def pasajero_modificar(request, id_pasajero):
    pasajero = get_object_or_404(Pasajero, id_pasajero=id_pasajero)
    if request.method == 'POST':
        form = FormularioPasajeroModificar(request.POST, instance=pasajero)  # Usar nuevo formulario
        if form.is_valid():
            form.save()
            return redirect('pasajero_detalles', id_pasajero=pasajero.id_pasajero)
    else:
        form = FormularioPasajeroModificar(instance=pasajero)  # Usar nuevo formulario
    return render(request, 'pasajeros/pasajero_modificar.html', {'form': form, 'pasajero': pasajero})

#DELETE 
def pasajero_eliminar(request, id_pasajero):
    pasajero = get_object_or_404(Pasajero, id_pasajero=id_pasajero)
    if request.method == 'POST':
        pasajero.delete()
        return redirect('pasajeros_lista')
    return redirect('pasajeros_lista')

# ============ VISTAS VEHICULOS ============

#READ
def vehiculo_lista(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/vehiculo_lista.html', {'vehiculos': vehiculos})

#CREATE
def vehiculo_crear(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            return redirect('vehiculo_detalle', patente=vehiculo.patente)
    else:
        form = VehiculoForm()
    return render(request, 'vehiculos/vehiculo_crear.html', {'form': form})

#DETAIL (READ ONE)
def vehiculo_detalle(request, patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
    except Vehiculo.MultipleObjectsReturned:
        vehiculo = Vehiculo.objects.filter(patente=patente).first()
    except Vehiculo.DoesNotExist:
        return redirect('vehiculo_lista')
    
    return render(request, 'vehiculos/vehiculo_detalle.html', {'vehiculo': vehiculo})

#UPDATE
def vehiculo_modificar(request, patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
    except Vehiculo.MultipleObjectsReturned:
        vehiculo = Vehiculo.objects.filter(patente=patente).first()
    except Vehiculo.DoesNotExist:
        return redirect('vehiculo_lista')
    
    if request.method == 'POST':
        form = VehiculoModificarForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('vehiculo_detalle', patente=vehiculo.patente)
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = VehiculoModificarForm(instance=vehiculo)
    return render(request, 'vehiculos/vehiculo_modificar.html', {'form': form, 'vehiculo': vehiculo})

#DELETE 
def vehiculo_eliminar(request, patente):
    try:
        vehiculo = Vehiculo.objects.get(patente=patente)
    except Vehiculo.MultipleObjectsReturned:
        if request.method == 'POST':
            Vehiculo.objects.filter(patente=patente).delete()
            return redirect('vehiculo_lista')
        else:
            return redirect('vehiculo_lista')
    except Vehiculo.DoesNotExist:
        return redirect('vehiculo_lista')
    
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculo_lista')
    return redirect('vehiculo_lista')

# ============ VISTAS RUTAS/API ============

def ruta_home(request):
    return render(request, 'rutas/generador_rutas.html')


# TEST CONEXION DE DATOS PARA GENERAR VIAJE
def ruta_crear(request):
    if request.method == 'POST':
        """ form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save()
            return redirect('vehiculo_detalle', patente=vehiculo.patente) """
    if request.method == 'GET':
        pasajeros = Pasajero.objects.all()
        empresas = list(pasajeros.values_list('empresa_trabajo', flat=True).order_by('empresa_trabajo'))
        vehiculos = Vehiculo.objects.all()
        choferes = Chofer.objects.all()
        datos = {
            'empresas' : empresas,
            'pasajeros' : pasajeros,
            'vehiculos' : vehiculos,
            'choferes' : choferes,
        }
        return render(request, 'rutas/ruta_crear.html', datos)

# Paso 1 de creación de viaje - Seleccionar pasajeros
@login_required
def ruta_crear_seleccionar_pasajeros(request):
    if request.method == 'GET':
        ### === Formulario de seleccion de pasajeros === ###
        pasajeros = Pasajero.objects.all().order_by('empresa_trabajo','apellido','nombre')
        # Empresas
        empresas = set(pasajeros.values_list('empresa_trabajo', flat=True).order_by('empresa_trabajo'))
        empresas = list(set(map(str.upper, empresas)))
        
        # Pasajeros
        pasajero_info = []
        for pasajero in pasajeros:
            pasajero_info.append({
                'id': str(pasajero.id_pasajero),
                'nombre': pasajero.nombre,
                'apellido': pasajero.apellido,
                'empresa': pasajero.empresa_trabajo.upper(),
            })
        
        datos = {
            'empresas': empresas,
            'pasajero_info': pasajero_info
        }
        return render(request, 'rutas/ruta_crear_seleccionar1_pasajeros.html', datos)
    
    if request.method == 'POST':
        ### === Seleccion de pasajeros completa === ###

        # Obtener los pasajeros seleccionados
        opciones_elegidas = request.POST.getlist('choices')
        
        # Validar que los IDs recibidos son validos
        ids_validos = set(str(p.id_pasajero) for p in Pasajero.objects.all())
        opciones_validadas = [id for id in opciones_elegidas if id in ids_validos]

        #Crear grupo de pasajeros , luego agregar cada uno de los pasajeros al viaje
        grupo = Grupo_Pasajeros.objects.create()
        
        #Cambiar estado a seleccionando pasajeros
        grupo.estado_creacion_viaje = "1"
        grupo.save()

        for id_pasajero in opciones_validadas:
            grupo.pasajero.add(id_pasajero)
        
        #Cambiar estado a seleccionando choferes
        grupo.estado_creacion_viaje = "2"
        grupo.save()
        return redirect('ruta_crear_seleccionar2_choferes', id_grupo_pasajeros = grupo.id_grupo_pasajeros)

# Paso 2 de creación de viaje - Seleccionar choferes disponibles
@login_required
def ruta_crear_seleccionar_choferes(request, id_grupo_pasajeros):
    if request.method == 'GET':
        ### === Formulario de seleccion de pasajeros === ###
        try:
            # Obtener los datos de los pasajeros del grupo
            grupo_pasajeros = Grupo_Pasajeros.objects.get(pk=id_grupo_pasajeros)
            if grupo_pasajeros.estado_creacion_viaje == "2":
                lista_pasajeros = grupo_pasajeros.pasajero.all()
                cantidad_pasajeros = len(lista_pasajeros)

                # Obtener los datos del chofer junto al vehiculo asignado - 
                chofer_vehiculo = Chofer.objects.select_related("id_vehiculo")
                chofer_con_vehiculo = chofer_vehiculo.exclude(id_vehiculo__exact=None)
                chofer_sin_vehiculo = chofer_vehiculo.filter(id_vehiculo__exact=None)
                datos = {
                    "lista_pasajeros": lista_pasajeros,
                    "cantidad_pasajeros": cantidad_pasajeros,
                    "chofer_con_vehiculo": chofer_con_vehiculo,
                    "chofer_sin_vehiculo": chofer_sin_vehiculo,
                }
                return render(request, 'rutas/ruta_crear_seleccionar2_choferes.html', datos)
            else:
                return redirect('ruta_crear')
        except Exception as e: 
            print(e)
    
    ### === Seleccion de choferes completa === ###
    if request.method == 'POST':
        print("check")
        grupo_pasajeros = Grupo_Pasajeros.objects.get(pk=id_grupo_pasajeros)
        print(grupo_pasajeros.estado_creacion_viaje)
        # Verificar que el grupo creado esta en la fase de seleccion de choferes - Asi evitar que se acceda por la URL
        if grupo_pasajeros.estado_creacion_viaje == "2":
            # Obtener los choferes seleccionados
            choferes_elegidos = request.POST.getlist('choices')

            # Validar que los IDs recibidos son validos
            ids_validos = set(str(c.id_chofer) for c in Chofer.objects.all())
            choferes_validados = [id for id in choferes_elegidos if id in ids_validos]

            #Obtener el grupo para asingar los choferes
            #Agregar los choferes al grupo para poder hacer los calculos en el siguiente paso
            for id_chofer in choferes_validados:
                grupo_pasajeros.chofer.add(id_chofer)
            return redirect('ruta_crear_seleccionar2_choferes', id_grupo_pasajeros = id_grupo_pasajeros)
        if grupo_pasajeros.estado_creacion_viaje == "1":
            return redirect('ruta_crear_seleccionar2_choferes', id_grupo_pasajeros = id_grupo_pasajeros)
        else:
            return redirect('ruta_crear')

    

# TEST FUNCIONAMIENTO API
@login_required()
def testeo_api(request):
    api_key = settings.GOOGLE_MAPS_API_KEY
    
    if not api_key:
        return render(request, 'rutas/test_api.html', {
            'error': 'API Key de Google Maps no configurada',
            'error_body': 'Verifica que GOOGLE_MAPS_API_KEY esté en settings.py'
        })
    
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
    }
    
    data = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": -33.5036,
                    "longitude": -70.7597
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": -33.5108,
                    "longitude": -70.7441
                }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "es-ES",
        "units": "METRIC"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            response_data = response.json()
            return render(request, 'rutas/test_api.html', {'response_data': response_data})
        else:
            return render(request, 'rutas/test_api.html', {
                'error': f'Error {response.status_code}',
                'error_body': response.text
            })
            
    except Exception as e:
        return render(request, 'rutas/test_api.html', {
            'error': 'Error de conexión',
            'error_body': str(e)
        })
