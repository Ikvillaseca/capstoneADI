from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import Grupo_Pasajeros
from django.contrib.auth.decorators import user_passes_test



# En proceso de testeo, estoy intentando crear un decorador para poder lograr verificar el estadod el grupo, 
# y poder redirigir de manera acorde al sitio correcto
def validar_estado_grupo_requerido(estado_requerido):
    def decorator(view_function):
        @wraps(view_function)
        def wrapper(request, id_grupo_pasajeros, *args, **kwargs):
            try:
                grupo = Grupo_Pasajeros.objects.get(pk=id_grupo_pasajeros)

                # Mapeo de estados a rutas, asi puedo enlazar cada estado a una pagina deseada
                estados_rutas = {
                    "0": "ruta_crear_seleccionar1_pasajeros",
                    "1": "ruta_crear_seleccionar1_pasajeros",
                    "2": "ruta_crear_seleccionar2_choferes",
                    "3": "ruta_crear_seleccionar_confirmar",
                }

                #Verificar que el estado del grupo sea el requerido
                if grupo.estado_creacion_viaje == estado_requerido:
                    # Agregar el grupo al request para usarlo en la vista
                    request.grupo_pasajeros = grupo
                    return view_function(request, id_grupo_pasajeros, *args, **kwargs)
                
                # Redirigir al paso correcto
                if grupo.estado_creacion_viaje in estados_rutas:
                    messages.info(request, "Has sido redirigido al paso correcto para la creacion de este viaje, para volver presiona el boton 'Volver'")
                    print(f"Redirigido al paso {grupo.estado_creacion_viaje}.")
                    return redirect(estados_rutas[grupo.estado_creacion_viaje], id_grupo_pasajeros=id_grupo_pasajeros)
                
                else:
                    messages.error(request, "Estado del grupo no válido.")
                    return redirect('rutas')

            except Grupo_Pasajeros.DoesNotExist:
                messages.error(request, "El grupo de pasajeros no existe.")
                return redirect('rutas')
        return wrapper
    return decorator
    