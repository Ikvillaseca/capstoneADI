from django.contrib import admin
from django.urls import path, include
from RouteAnvil import views

urlpatterns = [
    path('', views.index, name='index'),
    path('choferes/', views.choferes, name='choferes'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('pasajeros/', views.pasajeros, name='pasajeros'),
    path('rutas/', views.rutas, name='rutas'),
    path('generar_ruta/', views.generar_ruta, name='generar_ruta'),

]
