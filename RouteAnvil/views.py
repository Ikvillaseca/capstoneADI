import requests
import json
from .viajes_direcciones import asignar_viajes, generar_imagen_clusters, geocoding_desde_direccion
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from collections import defaultdict
from .decorators import validar_estado_grupo_requerido
from .models import Chofer, Pasajero, Vehiculo, Parada, Grupo_Pasajeros, Viaje, Parada_Viaje, Pasajero_Viaje, Grupo_Pasajeros

from .forms import (
    VehiculoForm,
    VehiculoModificarForm,
    FormularioChofer,
    FormularioChoferModificar,
    FormularioPasajero,
    FormularioPasajeroModificar,
    FormularioParadero,
    FormularioParaderoModificar,
    FormularioDestinoViaje,
    ViajeInicioForm
)


# Create your views here.
def index(request):
    # Obtener estadísticas para mostrar en el dashboard
    context = {
        'total_pasajeros': Pasajero.objects.count(),
        'total_choferes': Chofer.objects.count(),
        'total_vehiculos': Vehiculo.objects.count(),
        'total_paraderos': Parada.objects.count(),
    }
    return render(request, 'index.html', context)


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



# ============ VISTAS PARADEROS ============

#READ
def paraderos_lista(request):
    paraderos = Parada.objects.all()
    return render(request, 'paraderos/paradero_lista.html', {'paraderos': paraderos})

#CREATE
def paradero_crear(request):
    if request.method == 'POST':
        form = FormularioParadero(request.POST)
        if form.is_valid():
            # Obtener direccion y calcular los datos que necesito usando la API de geocoding
            nombre = form.cleaned_data['nombre']  
            direccion = form.cleaned_data['direccion']
            tipo_parada = form.cleaned_data['tipo_parada'] 

            # Obtener los datos desde api geocoding
            lat, lon, cleaned_direccion, tipo_deducido = geocoding_desde_direccion(direccion)
            if form.cleaned_data['tipo_parada'] == 'X':
                tipo_parada = tipo_deducido

            # Crear objeto a partir de los datos obtenidos
            parada = Parada.objects.create(
                nombre=nombre,
                tipo_parada=tipo_parada,
                direccion=cleaned_direccion,
                latitud=lat,
                longitud=lon,
            )
            return redirect('paradero_detalles', id_ubicacion=parada.id_ubicacion)
        
    else:
        form = FormularioParadero(initial={'tipo_parada': 'X'})
    
    datos = {
        'form': form,
        'GOOGLE_MAPS_API_EMBED': settings.GOOGLE_MAPS_API_EMBED  
    }
    return render(request, 'paraderos/paradero_crear.html', datos)

def paradero_detalles(request, id_ubicacion):
    paradero = get_object_or_404(Parada, id_ubicacion=id_ubicacion)
    datos = {
        'paradero': paradero,
        'GOOGLE_MAPS_API_EMBED': settings.GOOGLE_MAPS_API_EMBED
    }
    return render(request, 'paraderos/paradero_detalles.html', datos)

#UPDATE
def paradero_modificar(request, id_ubicacion):
    paradero = get_object_or_404(Parada, id_ubicacion=id_ubicacion)
    
    if request.method == 'POST':
        form = FormularioParaderoModificar(request.POST, instance=paradero)
        if form.is_valid():
            form.save()
            return redirect('paradero_detalles', id_ubicacion=paradero.id_ubicacion)
    else:
        form = FormularioParaderoModificar(instance=paradero)
    
    datos = {
        'form': form, 
        'paradero': paradero,
        'GOOGLE_MAPS_API_EMBED': settings.GOOGLE_MAPS_API_EMBED
    }
    return render(request, 'paraderos/paradero_modificar.html', datos)
#DELETE 
def paradero_eliminar(request, id_ubicacion):
    paradero = get_object_or_404(Parada, id_ubicacion=id_ubicacion)
    if request.method == 'POST':
        paradero.delete()
        return redirect('paraderos_lista')
    return redirect('paraderos_lista')





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

# Paso 0 de creación de viaje - Seleccionar pasajeros
@login_required
def ruta_crear_inicio(request):
    if request.method == 'GET':
        form = ViajeInicioForm()
        datos = {
            'form' : form,
        }
        return render(request, 'rutas/ruta_crear_0_inicio.html', datos)
    
    if request.method == 'POST':
        form = ViajeInicioForm(request.POST)        
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.estado_creacion_viaje = "1"
            grupo.save()
            print(grupo)

            return redirect('ruta_crear_seleccionar1_pasajeros', id_grupo_pasajeros=grupo.id_grupo_pasajeros)
        else:
            # Devolver el form porque puede contener errores
            datos = {'form': form,}
            return render(request, 'rutas/ruta_crear_0_inicio.html', datos)




# Paso 1 de creación de viaje - Seleccionar pasajeros
@login_required
@validar_estado_grupo_requerido("1")
def ruta_crear_seleccionar_pasajeros(request, id_grupo_pasajeros):
    grupo = request.grupo_pasajeros 
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
        # Se genera el grupo por lo tanto el estado en esta view puede ser 0 o 1
        # Cambia a 2 cuando se envia a la siguiente view

        # Obtener los pasajeros seleccionados
        opciones_elegidas = request.POST.getlist('choices')
        
        # Validar que los IDs recibidos son validos
        ids_validos = set(str(p.id_pasajero) for p in Pasajero.objects.all())
        opciones_validadas = [id for id in opciones_elegidas if id in ids_validos]

        for id_pasajero in opciones_validadas:
            grupo.pasajero.add(id_pasajero)
        
        #Cambiar estado a seleccionando choferes
        grupo.estado_creacion_viaje = "2"
        grupo.save()
        return redirect('ruta_crear_seleccionar2_choferes', id_grupo_pasajeros = grupo.id_grupo_pasajeros)

# Paso 2 de creación de viaje - Seleccionar choferes disponibles
@login_required
@validar_estado_grupo_requerido("2")
def ruta_crear_seleccionar_choferes(request, id_grupo_pasajeros):
    # Obtiene el grupo desde el decorator
    grupo = request.grupo_pasajeros 
    if request.method == 'GET':
        ### === Formulario de seleccion de pasajeros === ###
        # Obtener los datos de los pasajeros del grupo
        lista_pasajeros = grupo.pasajero.all()
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
        
    ### === Seleccion de choferes completa === ###
    if request.method == 'POST':
        # Verificar que el grupo creado esta en la fase de seleccion de choferes - Asi evitar que se acceda por la URL
        # Obtener los choferes seleccionados
        choferes_elegidos = request.POST.getlist('choices')

        # Validar que los IDs recibidos son validos
        ids_validos = set(str(c.id_chofer) for c in Chofer.objects.all())
        choferes_validados = [id for id in choferes_elegidos if id in ids_validos]

        #Obtener el grupo para asingar los choferes
        #Agregar los choferes al grupo para poder hacer los calculos en el siguiente paso
        for id_chofer in choferes_validados:
            grupo.chofer.add(id_chofer)

        #Cambiar estado a confirmacion de choferes
        grupo.estado_creacion_viaje = "3"
        grupo.save()

        return redirect('ruta_crear_seleccionar_confirmar', id_grupo_pasajeros = id_grupo_pasajeros)
        
# Paso 3 de creación de viaje - Confirmar seleccion
@login_required
@validar_estado_grupo_requerido("3")
def ruta_crear_seleccionar_confirmar(request, id_grupo_pasajeros):
    grupo = request.grupo_pasajeros

    if request.method == "GET":
        form = FormularioDestinoViaje()
        lista_pasajeros = grupo.pasajero.select_related("paradero_deseado").all()
        cantidad_pasajeros = len(lista_pasajeros)
        lista_choferes_vehiculo = grupo.chofer.all().select_related("id_vehiculo")

        paraderos_contador = defaultdict(list)
        for pasajero in lista_pasajeros:
            if pasajero.paradero_deseado:
                paradero_id = pasajero.paradero_deseado.id_ubicacion
                paraderos_contador[paradero_id].append(pasajero)

        lista_paraderos = []
        for paradero_id, pasajeros in paraderos_contador.items():
            paradero = pasajeros[0].paradero_deseado
            string_paradero = f"{len(pasajeros)} pasajeros => {paradero.nombre}"
            lista_paraderos.append(string_paradero)

        datos = {
            "form": form,
            "grupo": grupo, 
            "lista_pasajeros": lista_pasajeros,
            "cantidad_pasajeros": cantidad_pasajeros,
            "lista_choferes_vehiculo": lista_choferes_vehiculo,
            "lista_paraderos": lista_paraderos,
            "id_grupo_pasajeros": id_grupo_pasajeros,
        }
        return render(request, 'rutas/ruta_crear_seleccionar3_confirmar.html', datos)

    if request.method == "POST":
        form = FormularioDestinoViaje(request.POST)

        if form.is_valid():
            try:
                # Obtener los datos del form
                punto_encuentro = form.get_punto_encuentro()
                tipo_viaje = grupo.tipo_viaje
                fecha_hora_deseada = grupo.fecha_hora_deseada
                tipo_hora_deseada = grupo.tipo_hora_deseada
                # Hacer el trabajo pesado
                ids_viajes = asignar_viajes(grupo, punto_encuentro, tipo_viaje, fecha_hora_deseada, tipo_hora_deseada)

                # Actualizar el estado del grupo para que solo me sirva visualizar, ya no modificar
                grupo.estado_creacion_viaje = "A"
                grupo.save()

                print(f"Se crearon {len(ids_viajes)} viajes de {tipo_viaje} con {tipo_hora_deseada} a las {fecha_hora_deseada} exitosamente")

                # Redirigir a página de resumen de viajes
                return redirect("viajes_resumen", id_grupo_pasajeros=id_grupo_pasajeros)
            except Exception as e:
                print(f"Error al crear viajes: {str(e)}")
                messages.error(request, f"Error al crear viajes: {str(e)}")
        else:
            messages.error(request, "Corrija los errores en el formulario")

        # Recargar datos
        lista_pasajeros = grupo.pasajero.select_related("paradero_deseado").all()
        cantidad_pasajeros = len(lista_pasajeros)
        lista_choferes_vehiculo = grupo.chofer.all().select_related("id_vehiculo")

        paraderos_contador = defaultdict(list)
        for pasajero in lista_pasajeros:
            if pasajero.paradero_deseado:
                paradero_id = pasajero.paradero_deseado.id_ubicacion
                paraderos_contador[paradero_id].append(pasajero)

        lista_paraderos = []
        for paradero_id, pasajeros in paraderos_contador.items():
            paradero = pasajeros[0].paradero_deseado
            lista_paraderos.append(f"{len(pasajeros)} pasajeros => {paradero.nombre}")

        datos = {
            "form": form,
            "grupo": grupo,
            "lista_pasajeros": lista_pasajeros,
            "cantidad_pasajeros": cantidad_pasajeros,
            "lista_choferes_vehiculo": lista_choferes_vehiculo,
            "lista_paraderos": lista_paraderos,
            "id_grupo_pasajeros": id_grupo_pasajeros,
        }
        return render(request, 'rutas/ruta_crear_seleccionar3_confirmar.html', datos)
    
@login_required
def viajes_lista(request):
    # Obtener el grupo desde la request
    # Filtrar los viajes creados a partir del grupo de creacion
    viajes = Viaje.objects.filter().select_related('id_vehiculo', 'id_chofer', 'punto_encuentro').prefetch_related(
        'paradas_viaje__id_parada', 'pasajero_viaje_set__id_pasajero'
    ).order_by('-fecha_creacion')  # Más recientes primero
    
    # Preparar datos detallados
    viajes_detallados = []
    for viaje in viajes:
        paradas = viaje.paradas_viaje.all().order_by('orden')
        pasajeros = viaje.pasajero_viaje_set.all().select_related('id_pasajero')
        
        viajes_detallados.append({
            'viaje': viaje,
            'paradas': paradas,
            'pasajeros': pasajeros,
            'cantidad_pasajeros': pasajeros.count(),
            'cantidad_paradas': paradas.count(),
        })
    
    datos = {
        'viajes_detallados': viajes_detallados,
        'total_viajes': len(viajes_detallados),
    }
    
    return render(request, 'rutas/viajes_lista.html', datos)

# Nueva vista para mostrar resumen de viajes
@login_required
def viajes_resumen(request, id_grupo_pasajeros):
    # Obtener el grupo desde la request
    grupo = get_object_or_404(Grupo_Pasajeros, id_grupo_pasajeros=id_grupo_pasajeros)
    
    # Filtrar los viajes creados a partir del grupo de creacion
    viajes = Viaje.objects.filter(id_grupo=grupo).select_related('id_vehiculo', 'id_chofer', 'punto_encuentro').prefetch_related(
        'paradas_viaje__id_parada', 'pasajero_viaje_set__id_pasajero'
    ).order_by('-fecha_creacion')  # Más recientes primero
    
    # Preparar datos detallados
    viajes_detallados = []
    for viaje in viajes:
        paradas = viaje.paradas_viaje.all().order_by('orden')
        pasajeros = viaje.pasajero_viaje_set.all().select_related('id_pasajero')
        
        viajes_detallados.append({
            'viaje': viaje,
            'paradas': paradas,
            'pasajeros': pasajeros,
            'cantidad_pasajeros': pasajeros.count(),
            'cantidad_paradas': paradas.count(),
        })
    
    datos = {
        'grupo': grupo,
        'viajes_detallados': viajes_detallados,
        'total_viajes': len(viajes_detallados),
    }
    
    return render(request, 'rutas/viajes_resumen.html', datos)

# OK
# Vista detalle individual de viaje
@login_required
def viaje_detalle(request, id_viaje):
    # Obtener el viaje desde la request
    viaje = get_object_or_404(Viaje.objects.select_related("id_vehiculo", "id_chofer", "punto_encuentro"), id_viaje=id_viaje)

    # Ordenar paraderos - obtener ubicacion
    paradas = viaje.paradas_viaje.all().order_by("orden").select_related("id_parada")

    # Obtener pasajero con su paradero deseado
    pasajeros = viaje.pasajero_viaje_set.all().select_related(
        "id_pasajero__paradero_deseado"
    )

    datos = {
        "viaje": viaje,
        "paradas": paradas,
        "pasajeros": pasajeros,
    }
    return render(request, "rutas/viaje_detalle.html", datos)


# Vista para mostrar el itinerario del chofer
def vista_itinerario_chofer(request, id_chofer):
    chofer = get_object_or_404(Chofer, id_chofer=id_chofer)

    viajes_asignados = (
        Viaje.objects.filter(id_chofer=id_chofer)
        .select_related("id_vehiculo", "id_chofer", "punto_encuentro")
        .prefetch_related("paradas_viaje__id_parada", "pasajero_viaje_set__id_pasajero")
        .order_by("-fecha_creacion")
    )  # Más recientes primero

    # Preparar datos detallados
    viajes_detallados = []
    for viaje in viajes_asignados:
        paradas = viaje.paradas_viaje.all().order_by('orden')
        pasajeros = viaje.pasajero_viaje_set.all().select_related('id_pasajero')
        
        viajes_detallados.append({
            'viaje': viaje,
            'paradas': paradas,
            'pasajeros': pasajeros,
            'cantidad_pasajeros': pasajeros.count(),
            'cantidad_paradas': paradas.count(),
        })
    
    datos = {
        "chofer" : chofer,
        'viajes_detallados': viajes_detallados,
    }
   
    return render(request, "vista_chofer/vista_chofer.html", datos)


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

@login_required
def generar_imagen_presentacion(request, id_grupo_pasajeros):
    grupo = get_object_or_404(Grupo_Pasajeros, id_grupo_pasajeros=id_grupo_pasajeros)
    
    # Verificar que el grupo tenga viajes creados
    if grupo.estado_creacion_viaje != "A":
        messages.error(request, "Debe completar la creación de viajes antes de generar la visualización")
        return redirect('ruta_crear_seleccionar_confirmar', id_grupo_pasajeros=id_grupo_pasajeros)
    
    # Obtener el punto de encuentro desde los viajes creados
    viaje_ejemplo = Viaje.objects.filter(id_grupo=grupo).first()
    
    if not viaje_ejemplo:
        messages.error(request, "No se encontraron viajes para este grupo")
        return redirect('viajes_resumen', id_grupo_pasajeros=id_grupo_pasajeros)
    
    punto_encuentro = viaje_ejemplo.punto_encuentro
    
    # Generar imagen
    ruta_imagen = generar_imagen_clusters(
        grupo, 
        punto_encuentro, 
        f'cluster_grupo_{id_grupo_pasajeros}.png'
    )
    
    # Servir la imagen
    from django.http import FileResponse
    return FileResponse(open(ruta_imagen, 'rb'), content_type='image/png')

def chofer_dashboard(request):
    datos = {
    }
    return render(request, 'choferes/dashboard/index.html', datos)