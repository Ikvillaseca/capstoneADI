from django.urls import path
from RouteAnvil import views

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),
    
    # URLs para choferes
    path('choferes/', views.chofer_lista, name='chofer_lista'),
    path('chofer/crear/', views.chofer_crear, name='chofer_crear'),
    path('chofer/detalle/<uuid:id_chofer>/', views.chofer_detalle, name='chofer_detalle'),
    path('chofer/modificar/<uuid:id_chofer>/', views.chofer_modificar, name='chofer_modificar'),
    path('chofer/eliminar/<uuid:id_chofer>/', views.chofer_eliminar, name='chofer_eliminar'),
    
    # URLs para pasajeros
    path('pasajeros/', views.pasajeros_lista, name='pasajeros_lista'),
    path('pasajero/crear/', views.pasajero_crear, name='pasajero_crear'),
    path('pasajero/detalles/<uuid:id_pasajero>/', views.pasajero_detalles, name='pasajero_detalles'),
    path('pasajero/modificar/<uuid:id_pasajero>/', views.pasajero_modificar, name='pasajero_modificar'),
    path('pasajero/eliminar/<uuid:id_pasajero>/', views.pasajero_eliminar, name='pasajero_eliminar'),
    
    # URLs para vehículos
    path('vehiculos/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculo/crear/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculo/detalle/<str:patente>/', views.vehiculo_detalle, name='vehiculo_detalle'),
    path('vehiculo/modificar/<str:patente>/', views.vehiculo_modificar, name='vehiculo_modificar'),
    path('vehiculo/eliminar/<str:patente>/', views.vehiculo_eliminar, name='vehiculo_eliminar'),

    # URLs para paraderos
    path('paraderos/', views.paraderos_lista, name='paraderos_lista'),
    path('paradero/crear/', views.paradero_crear, name='paradero_crear'),
    path('paradero/detalles/<uuid:id_ubicacion>/', views.paradero_detalles, name='paradero_detalles'),
    path('paradero/modificar/<uuid:id_ubicacion>/', views.paradero_modificar, name='paradero_modificar'),
    path('paradero/eliminar/<uuid:id_ubicacion>/', views.paradero_eliminar, name='paradero_eliminar'),

    # URLs para rutas
    path('rutas/', views.ruta_home, name='rutas'),
    path('ruta/crear/', views.ruta_crear, name='ruta_crear'),
    path('ruta/crear/pasajeros/', views.ruta_crear_seleccionar_pasajeros, name='ruta_crear_seleccionar1_pasajeros'),
    path('ruta/crear/choferes/<int:id_grupo_pasajeros>/', views.ruta_crear_seleccionar_choferes, name='ruta_crear_seleccionar2_choferes'),
    path('ruta/crear/confirmacion/<int:id_grupo_pasajeros>/', views.ruta_crear_seleccionar_confirmar, name='ruta_crear_seleccionar_confirmar'),
    path('ruta/testeo-api/', views.testeo_api, name='testeo_api'),
]