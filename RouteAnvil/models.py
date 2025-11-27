import uuid
from django.db import models
from django.core.exceptions import ValidationError
from .choices import estado, tipo_licencia, parada, estado_creacion_viaje, tipo_viaje, tipo_hora_deseada

# Create your models here.

#Tabla de destinos posibles
class Parada(models.Model):
    id_ubicacion = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Ubicación")
    nombre = models.CharField(max_length=90, verbose_name="Nombre del Lugar")
    tipo_parada = models.CharField(max_length=1, choices=parada, verbose_name="Tipo de Parada")
    direccion = models.CharField(max_length=200, verbose_name="Dirección del Lugar")
    latitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud")

    def __str__(self):
        return f"{self.nombre} - {self.tipo_parada}: {self.direccion}"

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
    paradero_deseado = models.ForeignKey(Parada, on_delete=models.SET_NULL, null=True, blank=True, related_name='paradero_deseado',verbose_name="Paradero deseado")
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def get_paradero_deseado_display(self):
        if self.paradero_deseado:
            return str(self.paradero_deseado.nombre)
        return "Sin paradero asignado"
    
# Creada en el primer paso cuando se seleccionan pasajeros (Simplifica la consulta de pasajeros que van en la creación del viaje, y evita la repeticion de muchos datos)
class Grupo_Pasajeros(models.Model):
    id_grupo_pasajeros = models.AutoField(primary_key=True, verbose_name="ID Reserva")
    pasajero = models.ManyToManyField(Pasajero, verbose_name=("Pasajeros"), blank=True)
    chofer = models.ManyToManyField(Chofer, verbose_name=("Choferes"), blank=True)
    estado_creacion_viaje = models.CharField(max_length=1, choices=estado_creacion_viaje, default='0', verbose_name="Estado de creacion")
    fecha_hora_deseada = models.DateTimeField(blank=True)
    tipo_viaje = models.CharField(max_length=10, choices=tipo_viaje, default='IDA')
    tipo_hora_deseada = models.CharField(max_length=10, choices=tipo_hora_deseada, default='LLEGADA')
    def __str__(self):
        return f"Grupo {self.id_grupo_pasajeros}"

#Tabla Viajes 
class Viaje(models.Model):    
    id_viaje = models.AutoField(primary_key=True)
    tipo_viaje = models.CharField(max_length=10, choices=tipo_viaje, default='IDA')
    hora_salida = models.DateTimeField()
    hora_llegada = models.DateTimeField()
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    punto_encuentro = models.ForeignKey(Parada, on_delete=models.CASCADE, related_name='viajes_punto_encuentro')
    id_grupo = models.ForeignKey(Grupo_Pasajeros, on_delete=models.CASCADE, related_name='viajes', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    # punto_encuentro puede ser origen (si tipo=VUELTA) o destino (si tipo=IDA)
    
    def __str__(self):
        vehiculo_str = self.id_vehiculo.patente if self.id_vehiculo else "Sin Vehículo"
        return f"Viaje {self.id_viaje} - {self.id_viaje} ({vehiculo_str})"


class Parada_Viaje(models.Model):
    id_parada_viaje = models.AutoField(primary_key=True)
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, related_name='paradas_viaje')
    id_parada = models.ForeignKey(Parada, on_delete=models.CASCADE)
    orden = models.IntegerField()
    pasajeros_suben = models.IntegerField(default=0)
    pasajeros_bajan = models.IntegerField(default=0)
    hora_estimada_llegada = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['orden']
        unique_together = ['id_viaje', 'orden']
    
    def __str__(self):
        return f"Parada {self.orden} - Viaje {self.id_viaje.id_viaje}"

# Tabla Reservas
class Pasajero_Viaje(models.Model):
    id_reserva = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name="ID Reserva")
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name="Pasajero")
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name="Viaje")

    def __str__(self):
        return f"Reserva {self.id_reserva} - Pasajero {self.id_pasajero} en Viaje {self.id_viaje}"



