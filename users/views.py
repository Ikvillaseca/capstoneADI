from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import administrador_requerido, chofer_requerido
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirigir según el tipo de usuario
            if user.groups.filter(name='Choferes').exists():
                messages.success(request, f'Bienvenido {user.first_name}!')
                return redirect('chofer_dashboard')
            elif user.groups.filter(name='Administradores').exists():
                messages.success(request, f'Bienvenido Administrador {user.first_name}!')
                return redirect('index')
            else:
                #ARREGLO TEMPORAL
                messages.success(request, f'Bienvenido Administrador {user.first_name}!')
                return redirect('index')
                ###
                messages.warning(request, 'No tienes permisos asignados')
                logout(request)
                return redirect('login')
        else:
            messages.error(request, 'Email o contraseña incorrectos')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('index')
