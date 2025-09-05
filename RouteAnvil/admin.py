from django.contrib import admin
from .models import Chofer, Destino, Origen, Pasajero, Reserva, Vehiculo, Viaje

# Register your models here.

#Modelos de RouteAnvil
admin.site.register(Chofer)
admin.site.register(Destino)
admin.site.register(Origen)
admin.site.register(Pasajero)
admin.site.register(Reserva)
admin.site.register(Vehiculo)
admin.site.register(Viaje)