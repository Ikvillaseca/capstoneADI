from django.db import models
from .choices import estado

# Create your models here.

#Tabla Origen del viaje 
class Origen(models.Model):
    id_origen = models.AutoField(primary_key=True, verbose_name="ID Origen")
    nombre_origen = models.CharField(max_length=45, verbose_name="Nombre Origen")
    comuna = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_origen



#Tabla Destino del viaje
class Destino(models.Model):
    id_destino = models.AutoField(primary_key=True, verbose_name="ID Destino")
    nombre_destino = models.CharField(max_length=45, verbose_name="Nombre Destino")
    comuna = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_destino



#Tabla Choferes 
class Chofer(models.Model):
    id_chofer = models.AutoField(primary_key=True, verbose_name="ID Chofer")
    rut = models.CharField(max_length=12, verbose_name="RUT")
    nombre = models.CharField(max_length=45, verbose_name="Nombre")
    apellido = models.CharField(max_length=45, verbose_name="Apellido")
    tipo_licencia = models.CharField(max_length=45, verbose_name="Tipo de Licencia")
    direccion = models.CharField(max_length=45, verbose_name="Direccion")
    fecha_ultimo_control = models.DateField(verbose_name="Fecha Ultimo Control")
    fecha_proximo_control = models.DateField(verbose_name="Fecha Proximo Control")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"



#Tabla Vehiculos
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True, verbose_name="ID Vehiculo")
    patente = models.CharField(max_length=7, verbose_name="Patente")
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
    rut = models.CharField(max_length=12, verbose_name="RUT")
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
    id_origen = models.ForeignKey(Origen, on_delete=models.CASCADE, verbose_name="Origen")
    id_destino = models.ForeignKey(Destino, on_delete=models.CASCADE, verbose_name="Destino")

    def __str__(self):
        return f"Viaje {self.id_viaje} - {self.origen} hacia {self.destino}"
    


#Tabla Reservas
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, verbose_name="ID Reserva")
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name="Pasajero")
    id_viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name="Viaje")

    def __str__(self):
        return f"Reserva {self.id_reserva} - Pasajero {self.id_pasajero} para Viaje {self.id_Viaje}"

