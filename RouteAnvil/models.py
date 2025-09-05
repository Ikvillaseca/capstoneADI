from django.db import models
from .choices import estado

# Create your models here.

#Tabla Origen del viaje 
class Origen(models.Model):
    id_Origen = models.AutoField(primary_key=True, verbose_name="ID Origen")
    Nombre_Origen = models.CharField(max_length=45, verbose_name="Nombre Origen")
    Comuna = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_Origen



#Tabla Destino del viaje
class Destino(models.Model):
    id_Destino = models.AutoField(primary_key=True, verbose_name="ID Destino")
    Nombre_Destino = models.CharField(max_length=45, verbose_name="Nombre Destino")
    Comuna = models.CharField(max_length=45, verbose_name="Comuna")

    def __str__(self):
        return self.nombre_Destino



#Tabla Choferes 
class Chofer(models.Model):
    id_Chofer = models.AutoField(primary_key=True, verbose_name="ID Chofer")
    Rut = models.CharField(max_length=12, verbose_name="RUT")
    Nombre = models.CharField(max_length=45, verbose_name="Nombre")
    Apellido = models.CharField(max_length=45, verbose_name="Apellido")
    Tipo_Licencia = models.CharField(max_length=45, verbose_name="Tipo de Licencia")
    Direccion = models.CharField(max_length=45, verbose_name="Direccion")
    Fecha_Ultimo_Control = models.DateField(verbose_name="Fecha Ultimo Control")
    Fecha_Proximo_Control = models.DateField(verbose_name="Fecha Proximo Control")

    def __str__(self):
        return f"{self.Nombre} {self.Apellido}"



#Tabla Vehiculos
class Vehiculo(models.Model):
    id_Vehiculo = models.AutoField(primary_key=True, verbose_name="ID Vehiculo")
    Patente = models.CharField(max_length=7, verbose_name="Patente")
    Marca = models.CharField(max_length=45, verbose_name="Marca")
    Capacidad = models.IntegerField(verbose_name="Capacidad")
    Estado = models.CharField(max_length=1, choices=estado, default='A', verbose_name="Estado")
    Revision_Tecnica = models.DateField(verbose_name="Revision Tecnica")
    Proxima_Revision = models.DateField(verbose_name="Proxima Revision")

    def __str__(self):
        return self.Patente



#Tabla Pasajeros
class Pasajero(models.Model):
    id_Pasajero = models.AutoField(primary_key=True, verbose_name="ID Pasajero")
    Rut = models.CharField(max_length=12, verbose_name="RUT")
    Nombre = models.CharField(max_length=45, verbose_name="Nombre")
    Apellido = models.CharField(max_length=45, verbose_name="Apellido")
    Telefono = models.CharField(max_length=15, verbose_name="Telefono")
    Empresa_Trabajo = models.CharField(max_length=45, verbose_name="Empresa de Trabajo")

    def __str__(self):
        return f"{self.Nombre} {self.Apellido}"
    


#Tabla Viajes 
class Viaje(models.Model):
    id_Viaje = models.AutoField(primary_key=True, verbose_name="ID Viaje")
    Fecha = models.DateField(verbose_name="Fecha del Viaje")
    Hora_Salida = models.DateTimeField(verbose_name="Hora de Salida")
    Hora_Llegada = models.DateTimeField(verbose_name="Hora de Llegada")
    id_Vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, verbose_name="Vehiculo")
    id_Chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE, verbose_name="Chofer")
    id_Origen = models.ForeignKey(Origen, on_delete=models.CASCADE, verbose_name="Origen")
    id_Destino = models.ForeignKey(Destino, on_delete=models.CASCADE, verbose_name="Destino")

    def __str__(self):
        return f"Viaje {self.id_Viaje} - {self.Origen} hacia {self.Destino}"
    


#Tabla Reservas
class Reserva(models.Model):
    id_Reserva = models.AutoField(primary_key=True, verbose_name="ID Reserva")
    id_pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, verbose_name="Pasajero")
    id_Viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE, verbose_name="Viaje")

    def __str__(self):
        return f"Reserva {self.id_Reserva} - Pasajero {self.id_pasajero} para Viaje {self.id_Viaje}"

