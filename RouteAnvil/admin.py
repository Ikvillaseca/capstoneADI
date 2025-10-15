from django.contrib import admin
from .models import Chofer, Empresa, Punto_toma_pasajero, Pasajero, Reserva, Vehiculo, Viaje

# Register your models here.

#Modelos de RouteAnvil
admin.site.register(Chofer)
admin.site.register(Empresa)
admin.site.register(Punto_toma_pasajero)
admin.site.register(Pasajero)
admin.site.register(Reserva)
admin.site.register(Vehiculo)
admin.site.register(Viaje)