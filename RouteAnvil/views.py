from django.shortcuts import render

#Aqui definimos cada vista de django (backend en python)
def index(request):
    return render(request, 'index.html')


def choferes(request):
    return render(request, 'choferes.html')

def vehiculos(request):
    return render(request, 'vehiculos.html')

def pasajeros(request):
    return render(request, 'pasajeros.html')

def rutas(request):
    return render(request, 'rutas.html')

def destinos(request):
    return render(request, 'destinos.html')



def generar_ruta(request):
    return render(request, 'generar_ruta.html')
