from django.contrib import admin
from django.urls import path, include
from RouteAnvil import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('pasajeros/', views.pasajeros, name='pasajeros'),
    path('destinos/', views.destinos, name='destinos'),
    path('rutas/', views.rutas, name='rutas'),
    path('generar_ruta/', views.generar_ruta, name='generar_ruta'),




    #urls para las paginas relacionas con el chofer
    path('choferes/', views.choferes_lista, name='chofer_lista'),
    path('chofer/detalle/<int:id>/', views.chofer_detalle, name='chofer_detalle'),
    path('chofer/crear/', views.chofer_crear, name='chofer_crear'),
    path('chofer/modificar/<int:id>/', views.chofer_modificar, name='chofer_modificar'),
    path('chofer/eliminar/<int:id>/', views.chofer_eliminar, name='chofer_eliminar'),
]
