# Estados para vehiculos
estado = (
    ("A", "Activo"),
    ("I", "Inactivo"),
    ("M", "Mantenimiento"),
    ("E", "En Ruta"),
)

# Tipos licencia para choferes
tipo_licencia = (
    ("A1", "Licencia Clase A1"),
    ("A2", "Licencia Clase A2"),
    ("A3", "Licencia Clase A3"),
    ("A4", "Licencia Clase A4"),
    ("A5", "Licencia Clase A5"),
    ("B", "Licencia Clase B"),

)


# Destinos de viajes
parada = (
    ("M", "Metro"),
    ("E", "Empresa"),
    ("H", "Hotel"),
    ("A", "Aeropuerto"),
    ("P", "Paradero"),
    ("O", "Otro"),
)

estado_creacion_viaje = (
    ("0", "Estado NULO"),
    ("1", "Seleccionando Pasajeros"),
    ("2", "Seleccionando Choferes"),
    ("3", "Confirmando Viaje"),
    ("A", "Viajes Creados"),
)