from django.contrib import admin
from django.urls import path, include
from RouteAnvil import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destinos/', views.destinos, name='destinos'),
    path('rutas/', views.rutas, name='rutas'),
    path('generar_ruta/', views.generar_ruta, name='generar_ruta'),
    path('testeo-api/', views.test_api, name='testeo_api'),


    path('pasajeros/', views.pasajeros_lista, name='pasajeros_lista'),
    path('pasajero/crear/', views.pasajero_crear, name='pasajero_crear'),
    path('pasajero/detalles/<int:id>', views.pasajero_detalles, name='pasajero_detalles'),
    path('pasajero/modificar/<int:id>', views.pasajero_modificar, name='pasajero_modificar'),
    path('pasajero/eliminar/<int:id>', views.pasajero_eliminar, name='pasajero_eliminar'),




    #urls para las paginas relacionas con el chofer
    path('choferes/', views.choferes_lista, name='chofer_lista'),
    path('chofer/detalle/<int:id>/', views.chofer_detalle, name='chofer_detalle'),
    path('chofer/crear/', views.chofer_crear, name='chofer_crear'),
    path('chofer/modificar/<int:id>/', views.chofer_modificar, name='chofer_modificar'),
    path('chofer/eliminar/<int:id>/', views.chofer_eliminar, name='chofer_eliminar'),

   #urls para las paginas relacionadas con el vehiculo
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('vehiculos_crear/', views.vehiculo_crear, name='vehiculo_crear'),
    path('buscar_vehiculo/', views.buscar_vehiculo, name='vehiculo_detalle'),
    path('vehiculos_modificar/<int:pk>/', views.vehiculo_modificar, name='vehiculo_modificar'),
    path('vehiculo_lista/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculos_eliminar/<int:pk>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
]
