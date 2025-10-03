from django.contrib import admin
from django.urls import path, include
from RouteAnvil import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destinos/', views.destinos, name='destinos'),
    path('rutas/', views.rutas, name='rutas'),
    path('generar_ruta/', views.generar_ruta, name='generar_ruta'),
    path('testeo-api/', views.test_api, name='testeo_api'),

    # URLs de Pasajeros
    path('pasajeros/', views.pasajeros_lista, name='pasajeros_lista'),
    path('pasajero/crear/', views.pasajero_crear, name='pasajero_crear'),
    path('pasajero/detalles/<int:id>', views.pasajero_detalles, name='pasajero_detalles'),
    path('pasajero/modificar/<int:id>', views.pasajero_modificar, name='pasajero_modificar'),
    path('pasajero/eliminar/<int:id>', views.pasajero_eliminar, name='pasajero_eliminar'),

    # URLs de Choferes
    path('choferes/', views.choferes_lista, name='chofer_lista'),
    path('chofer/detalle/<int:id>/', views.chofer_detalle, name='chofer_detalle'),
    path('chofer/crear/', views.chofer_crear, name='chofer_crear'),
    path('chofer/modificar/<int:id>/', views.chofer_modificar, name='chofer_modificar'),
    path('chofer/eliminar/<int:id>/', views.chofer_eliminar, name='chofer_eliminar'),

    # URLs de Vehículos
    path('vehiculo_lista/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculo_crear/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculo/detalle/<str:patente>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculo/modificar/<str:patente>/', views.vehiculo_modificar, name='vehiculo_modificar'),
    path('vehiculo/eliminar/<str:patente>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
    path('buscar_vehiculo/', views.buscar_vehiculo, name='buscar_vehiculo'), 
]
