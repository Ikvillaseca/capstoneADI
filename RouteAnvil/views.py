from django.shortcuts import render, get_object_or_404
from .models import Pasajero

#Aqui definimos cada vista de django (backend en python)
def index(request):
    return render(request, 'index.html')


def choferes(request):
    return render(request, 'choferes.html')

def vehiculos(request):
    return render(request, 'vehiculos.html')

def rutas(request):
    return render(request, 'rutas.html')

def destinos(request):
    return render(request, 'destinos.html')



def generar_ruta(request):
    return render(request, 'generar_ruta.html')



# == PASAJEROS CRUD / VISTAS ==
#Listar (READ *)
def pasajeros_lista(request):
    pasajeros = Pasajero.objects.all()
    data = {
        'pasajeros' : pasajeros,
    }
    return render(request, 'pasajeros/pasajeros_lista.html', data)

#Crear (CREATE)
def pasajero_crear(request):
    return render(request, 'pasajeros/pasajero_crear.html')

#Detalles (READ)
def pasajero_detalles(request, id):
    pasajero =  get_object_or_404(Pasajero, id_Pasajero=id)
    data = {
        'pasajero' : pasajero,
    }
    return render(request, 'pasajeros/pasajero_detalles.html', data)

#Modificar (UPDATE)
def pasajero_modificar(request, id):
    return render(request, 'pasajeros/pasajero_modificar.html')

#Eliminar (DELETE)
def pasajero_eliminar(request, id):
    return render(request, 'pasajeros/pasajero_eliminar.html')

