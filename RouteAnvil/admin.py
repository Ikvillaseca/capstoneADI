from django.contrib import admin
from .models import Chofer,Grupo_Pasajeros, Pasajero, Pasajero_Viaje, Vehiculo, Viaje, Ubicacion

# Register your models here.

#Modelos de RouteAnvil
admin.site.register(Chofer)
admin.site.register(Ubicacion)
admin.site.register(Pasajero)
admin.site.register(Pasajero_Viaje)
admin.site.register(Grupo_Pasajeros)
admin.site.register(Vehiculo)
admin.site.register(Viaje)