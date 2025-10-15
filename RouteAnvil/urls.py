from django.contrib import admin
from django.urls import path, include
from RouteAnvil import views

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # URLs para choferes
    path('choferes/', views.chofer_lista, name='chofer_lista'),
    path('chofer/crear/', views.chofer_crear, name='chofer_crear'),
    path('chofer/detalle/<int:id>/', views.chofer_detalle, name='chofer_detalle'),
    path('chofer/modificar/<int:id>/', views.chofer_modificar, name='chofer_modificar'),
    path('chofer/eliminar/<int:id>/', views.chofer_eliminar, name='chofer_eliminar'),
    
    # URLs para pasajeros
    path('pasajeros/', views.pasajeros_lista, name='pasajeros_lista'),
    path('pasajero/crear/', views.pasajero_crear, name='pasajero_crear'),
    path('pasajero/detalles/<int:id>/', views.pasajero_detalles, name='pasajero_detalles'),
    path('pasajero/modificar/<int:id>/', views.pasajero_modificar, name='pasajero_modificar'),
    path('pasajero/eliminar/<int:id>/', views.pasajero_eliminar, name='pasajero_eliminar'),
    
    # URLs para vehículos
    path('vehiculos/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculo/crear/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculo/detalle/<str:patente>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculo/modificar/<str:patente>/', views.vehiculo_modificar, name='vehiculo_modificar'),
    path('vehiculo/eliminar/<str:patente>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
    
    # URLs para rutas
    path('rutas/', views.ruta_home, name='rutas'),
    path('ruta/crear/', views.ruta_crear, name='ruta_crear'),
    path('ruta/testeo-api/', views.testeo_api, name='testeo_api'),
]