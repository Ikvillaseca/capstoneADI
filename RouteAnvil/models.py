from django.db import models
from .choices import estado, tipo_licencia

# Create your models here.

#Tabla Origen del viaje 
class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True, verbose_name="ID Empresa")
    nombre_empresa = models.CharField(max_length=45, verbose_name="Nombre Empresa")
    ubicacion = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_origen

#Tabla Destino del viaje
class Punto_toma_pasajero(models.Model):
    id_destino = models.AutoField(primary_key=True, verbose_name="ID Destino")
    parada = models.CharField(max_length=45, verbose_name="Nombre parada")
    comuna = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_destino

#Tabla Choferes 
class Chofer(models.Model):
    id_chofer = models.AutoField(primary_key=True, verbose_name="ID Chofer")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    apellido = models.CharField(max_length=45, verbose_name="Apellido")
    tipo_licencia = models.CharField(max_length=1, choices=tipo_licencia, verbose_name="Tipo de Licencia")  # Agregar choices
    direccion = models.CharField(max_length=45, verbose_name="Direccion")
    fecha_ultimo_control = models.DateField(verbose_name="Fecha Ultimo Control")
    fecha_proximo_control = models.DateField(verbose_name="Fecha Proximo Control")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#Tabla Vehiculos
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True, verbose_name="ID Vehiculo")
    patente = models.CharField(max_length=7, unique=True, verbose_name="Patente") 
    marca = models.CharField(max_length=45, verbose_name="Marca")
    capacidad = models.IntegerField(verbose_name="Capacidad")
    estado = models.CharField(max_length=1, choices=estado, default='A', verbose_name="Estado")
    revision_tecnica = models.DateField(verbose_name="Revision Tecnica")
    proxima_revision = models.DateField(verbose_name="Proxima Revision")

    def __str__(self):
        return self.patente

#Tabla Pasajeros
class Pasajero(models.Model):
    id_pasajero = models.AutoField(primary_key=True, verbose_name="ID Pasajero")
    rut = models.CharField(max_length=12, unique=True, verbose_name="RUT")  
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    apellido = models.CharField(max_length=45, verbose_name="Apellido")
    telefono = models.CharField(max_length=15, verbose_name="Telefono")
    empresa_trabajo = models.CharField(max_length=45, verbose_name="Empresa de Trabajo")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

#Tabla Viajes 
class Viaje(models.Model):
    id_viaje = models.AutoField(primary_key=True, verbose_name="ID Viaje")
    fecha = models.DateField(verbose_name="Fecha del Viaje")
    hora_Salida = models.DateTimeField(verbose_name="Hora de Salida")
    hora_Llegada = models.DateTimeField(verbose_name="Hora de Llegada")
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name="Vehiculo")
    id_chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, verbose_name="Chofer")
    id_origen = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name="Origen")
    id_destino = models.ForeignKey(Punto_toma_pasajero, on_delete=models.CASCADE, verbose_name="Destino")

    def __str__(self):
        return f"Viaje {self.id_viaje} - {self.id_origen} hacia {self.id_destino}"

#Tabla Reservas
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, verbose_name="ID Reserva")
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name="Pasajero")
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name="Viaje")

    def __str__(self):
        return f"Reserva {self.id_reserva} - Pasajero {self.id_pasajero} para Viaje {self.id_viaje}"

