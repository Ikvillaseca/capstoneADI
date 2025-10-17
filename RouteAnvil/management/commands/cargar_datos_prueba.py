import uuid
from django.core.management.base import BaseCommand
from RouteAnvil.models import Pasajero #, Chofer, Vehiculo, Viaje, Pasajero_Viaje

class Command(BaseCommand):
    help = "Llena datos iniciales en la base de datos utiles para poder testear funcionalidad manualmente"

    def handle(self, *args, **options):
        self.stdout.write('Creando datos...')
        pasajeros_creados = 0
        pasajeros_existentes = 0

        #Aqui tengo mis datos de prueba los traje de una lista que me habia hecho en .txt
        datos_prueba_pasajero = [
            # Formato: rut, nombre, apellido, telefono, empresa
            ["24646811-7", "PFTESTUNO", "TEST", "+56900000001", "Falabella"],
            ["23458382-4", "PFTESTDOS", "TEST", "+56900000002", "Falabella"],
            ["16369291-0", "PFTESTTRES", "TEST", "+56900000003", "FalaBella"],
            ["21774266-8", "PFTESTCUATRO", "TEST", "+56900000004", "FALABELLA"],
            ["10408365-k", "PATESTCINCO", "TEST", "+56900000005", "ABCDIN"],
            ["10241599-k", "PATESTSEIS", "TEST", "+56900000006", "ABCDIN"],
            ["20531884-4", "PFTESTSIETE", "TEST", "+56900000007", "falabella"]
        ]

        #Creo un pasajero
        for dato_prueba in datos_prueba_pasajero:
            rut, nombre, apellido, telefono, empresa_trabajo = dato_prueba
            #Para evitar ingresar ruts que existen
            if Pasajero.objects.filter(rut=rut).exists():
                self.stdout.write(f"Pasajero con RUT {rut} ya existe. Omitiendo.")
                pasajeros_existentes +=1
            else:
                Pasajero.objects.create(
                        id_pasajero=uuid.uuid4(),
                        rut=rut,
                        nombre=nombre,
                        apellido=apellido,
                        telefono=telefono,
                        empresa_trabajo=empresa_trabajo
                    )
                pasajeros_creados += 1
                self.stdout.write(f"Creado pasajero: {nombre} {apellido} ({rut})")
        self.stdout.write(self.style.SUCCESS(f"Procesamiento completado: {pasajeros_creados} pasajeros creados, {pasajeros_existentes} omitidos"))
