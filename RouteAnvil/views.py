# Eliminar chofer (DELETE)
from django.views.decorators.http import require_POST
def chofer_eliminar(request, id):
    from .models import Chofer
    chofer = Chofer.objects.get(id_chofer=id)
    if request.method == 'POST':
        chofer.delete()
        return redirect('chofer_lista')
    return render(request, 'choferes/chofer_eliminar.html', {'chofer': chofer})
from django.shortcuts import render, redirect
from .models import Chofer
from django.shortcuts import get_object_or_404
from .models import Pasajero

#Aqui definimos cada vista de django (backend en python)
def index(request):
    return render(request, 'index.html')


def vehiculos(request):
    return render(request, 'vehiculos.html')

def rutas(request):
    return render(request, 'rutas.html')

def destinos(request):
    return render(request, 'destinos.html')



def generar_ruta(request):
    return render(request, 'generar_ruta.html')



#CHOFERES CRUD - VISTAS
#Listar (READ ALL)
def choferes_lista(request):
    choferes = Chofer.objects.all()
    data = {'choferes': choferes}
    return render(request, 'choferes/chofer_lista.html', data)



#Crear chofer (CREATE)
def chofer_crear(request):
    from .forms import FormularioChofer
    if request.method == 'POST':
        form = FormularioChofer(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chofer_lista')
    else:
        form = FormularioChofer()
    return render(request, 'choferes/chofer_crear.html', {'form': form})



#Detalle chofer (READ 1)
def chofer_detalle(request, id):
    chofer = Chofer.objects.get(id_chofer=id)
    data = {'chofer': chofer}
    return render(request, 'choferes/chofer_detalle.html', data)
    


#Modificar chofer (UPDATE)
def chofer_modificar(request, id):
    from .forms import FormularioChofer
    chofer = Chofer.objects.get(id_chofer=id)
    if request.method == 'POST':
        form = FormularioChofer(request.POST, instance=chofer)
        if form.is_valid():
            form.save()
            return redirect('chofer_detalle', id=chofer.id_chofer)
    else:
        form = FormularioChofer(instance=chofer)
    return render(request, 'choferes/chofer_modificar.html', {'form': form, 'chofer': chofer})



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
    from .forms import FormularioPasajero
    if request.method == 'POST':
        form = FormularioPasajero(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pasajeros_lista')
    else:
        form = FormularioPasajero()
    return render(request, 'pasajeros/pasajero_crear.html', {'form': form})

#Detalles (READ)
def pasajero_detalles(request, id):
    pasajero =  get_object_or_404(Pasajero, id_pasajero=id)
    data = {
        'pasajero' : pasajero,
    }
    return render(request, 'pasajeros/pasajero_detalles.html', data)

#Modificar (UPDATE)
def pasajero_modificar(request, id):
    from .forms import FormularioPasajero
    pasajero = Pasajero.objects.get(id_pasajero=id)
    if request.method == 'POST':
        form = FormularioPasajero(request.POST, instance=pasajero)
        if form.is_valid():
            form.save()
            return redirect('pasajero_detalles', id=pasajero.id_pasajero)
    else:
        form = FormularioPasajero(instance=pasajero)
    return render(request, 'pasajeros/pasajero_modificar.html', {'form': form, 'pasajero': pasajero})

#Eliminar (DELETE)
def pasajero_eliminar(request, id):
    pasajero = Pasajero.objects.get(id_pasajero=id)
    if request.method == 'POST':
        pasajero.delete()
        return redirect('pasajeros_lista')
    return render(request, 'pasajeros/pasajero_eliminar.html', {'pasajero': pasajero})

