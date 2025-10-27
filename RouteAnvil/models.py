import uuid
from django.db import models
from django.core.exceptions import ValidationError
from .choices import estado, tipo_licencia, parada

# Create your models here.

#Tabla de destinos posibles
class Ubicacion(models.Model):
    id_ubicacion = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Ubicacion")
    tipo_parada = models.CharField(max_length=1, choices=parada, verbose_name="Tipo de Parada")
    nombre = models.CharField(max_length=45, verbose_name="Nombre del Lugar")
    direccion = models.CharField(max_length=100, verbose_name="Direccion del Lugar")
    def __str__(self):
        return self.nombre

#Tabla Choferes 
class Chofer(models.Model):
    id_chofer = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Chofer")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    apellido = models.CharField(max_length=45, verbose_name="Apellido")
    tipo_licencia = models.CharField(max_length=2, choices=tipo_licencia, verbose_name="Tipo de Licencia") 
    direccion = models.CharField(max_length=45, verbose_name="Direccion")
    fecha_ultimo_control = models.DateField(verbose_name="Fecha Ultimo Control")
    fecha_proximo_control = models.DateField(verbose_name="Fecha Proximo Control")
    id_vehiculo = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vehiculo Asignado")
    
    def clean(self):
        # Validación para evitar vehículos duplicados
        super().clean()
        if self.id_vehiculo:
            # Verificar si otro chofer ya tiene este vehículo asignado
            otros_choferes = Chofer.objects.filter(id_vehiculo=self.id_vehiculo)
            if self.pk:
                otros_choferes = otros_choferes.exclude(pk=self.pk)
            
            if otros_choferes.exists():
                chofer_actual = otros_choferes.first()
                raise ValidationError({
                    'id_vehiculo': f'El vehículo {self.id_vehiculo.patente} ya está asignado a {chofer_actual.nombre} {chofer_actual.apellido}.'
                })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"

#Tabla Vehiculos
class Vehiculo(models.Model):
    id_vehiculo = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Vehiculo")
    patente = models.CharField(max_length=7, unique=True, verbose_name="Patente") 
    marca = models.CharField(max_length=45, verbose_name="Marca")
    modelo = models.CharField(max_length=45, verbose_name="Modelo")
    anio = models.IntegerField(verbose_name="Año")
    capacidad = models.IntegerField(verbose_name="Capacidad")
    estado = models.CharField(max_length=1, choices=estado, default='A', verbose_name="Estado")
    revision_tecnica = models.DateField(verbose_name="Revision Tecnica")
    proxima_revision = models.DateField(verbose_name="Proxima Revision")

    def __str__(self):
        return f"{self.patente}"

#Tabla Pasajeros
class Pasajero(models.Model):
    id_pasajero = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Pasajero")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")  
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    apellido = models.CharField(max_length=45, verbose_name="Apellido")
    telefono = models.CharField(max_length=15, verbose_name="Telefono")
    empresa_trabajo = models.CharField(max_length=45, verbose_name="Empresa de Trabajo")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#Tabla Viajes 
class Viaje(models.Model):
    id_viaje = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Viaje")
    fecha_creacion = models.DateField(verbose_name="Fecha de creacion del Viaje", auto_now_add=True)
    hora_Salida = models.TimeField(verbose_name="Hora de Salida")
    hora_Llegada = models.TimeField(verbose_name="Hora de Llegada")
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Vehiculo")    
    id_chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, verbose_name="Chofer")
    
    origen = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, verbose_name="Origen", related_name='viajes_origen')
    destino = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, verbose_name="Destino", related_name='viajes_destino')

    def __str__(self):
        vehiculo_str = self.id_vehiculo.patente if self.id_vehiculo else "Sin Vehículo"
        return f"Viaje {self.id_viaje} - {self.origen} → {self.destino} ({vehiculo_str})"


# Tabla Reservas
class Pasajero_Viaje(models.Model):
    id_reserva = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Reserva")
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name="Pasajero")
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name="Viaje")

    def __str__(self):
        return f"Reserva {self.id_reserva} - Pasajero {self.id_pasajero} en Viaje {self.id_viaje}"

# Tabla grupo de pasajeros
# Creada en el primer paso cuando se seleccionan pasajeros (Simplifica la consulta de pasajeros que van en la creación del viaje, y evita la repeticion de muchos datos)
class Grupo_Pasajeros(models.Model):
    id_grupo_pasajeros = models.AutoField(primary_key=True, verbose_name="ID Reserva")
    pasajero = models.ManyToManyField(Pasajero, verbose_name=("Pasajeros"))

    def __str__(self):
        return f"Grupo {self.id_grupo_pasajeros}"


