import uuid
from django.core.management.base import BaseCommand
from RouteAnvil.models import Pasajero, Parada, Chofer, Vehiculo, Viaje, Pasajero_Viaje

class Command(BaseCommand):
    help = "Llena datos iniciales en la base de datos utiles para poder testear funcionalidad manualmente"

    def handle(self, *args, **options):
        self.stdout.write('Creando datos...')
        pasajeros_creados = 0
        pasajeros_existentes = 0
        paraderos_creados = 0
        paraderos_existentes = 0
        vehiculos_creados = 0
        vehiculos_existentes = 0    
        choferes_creados = 0
        choferes_existentes = 0 


        datos_prueba_paraderos = [
            # Formato: nombre, tipo, direccion, latitud, longitud
            ["Plaza de maipu","Metro","Plaza de Maipú, Maipú, Región Metropolitana, Chile",-33.510520,-70.757230],
            ["Metro Tobalaba","Metro","Tobalaba, 7510005 Providencia, Región Metropolitana, Chile",-33.418088,-70.601887],
            ["metro las rejas","Metro","Las Rejas, Lo Prado, Estación Central, Región Metropolitana, Chile",-33.457457,-70.706325],
            ["Puente Cal y Canto","Metro","Puente Cal y Canto, Santiago, Región Metropolitana",-33.432689,-70.652090],
            ["Estación Central","Metro","Estación Central, 9160018 Santiago, Estación Central, Región Metropolitana",-33.451303,-70.678825],
            ["Los Héroes","Metro","Los Héroes, Santiago, Región Metropolitana",-33.446055,-70.660183],
            ["Plaza Egaña","Metro","Plaza Egaña, La Reina, Región Metropolitana",-33.453221,-70.570558],
        ]

        datos_prueba_vehiculos = [
            # Formato: patente, marca, modelo, año, capacidad_pasajeros, estado, revision_tecnica, proxima_revision
            ["ABCD12","Toyota","Hiace",2015,15,"A","2023-06-10","2024-06-10"],
            ["EFGH34","Mercedes-Benz","Sprinter",2018,20,"A","2020-08-15","2022-08-15"],
            ["IJKL56","Ford","Transit",2020,10,"A","2025-09-01","2028-09-01"],
            ["MNOP78","Renault","Master",2017,10,"M","2002-07-12","2010-07-12"],
            ["QRST90","Chevrolet","NPR",2019,5,"A","2023-11-20","2024-11-20"],
            ["RC9013","Hyundai","H350",2021,4,"M","2023-06-05","2024-06-05"],
        ]

        datos_prueba_choferes = [
            # Formato: rut, nombre, apellido, tipo_licencia, dirección, fecha_ultimo_control, fecha_proximo_control
            ["19532668-1","Juan","Pérez","Licencia Clase A3","Calle Falsa 123, Santiago","2023-02-12","2024-03-15"],
            ["12588673-6","María","González","Licencia Clase A2","Avenida Siempre Viva 742, Maipú","2022-06-20","2023-06-20"],
            ["13175300-4","Carlos","Ramírez","Licencia Clase A4","Calle del Sol 456, Providencia","2023-01-10","2024-01-10"],
            ["5479269-7","Ana","López","Licencia Clase A5","Pasaje Los Pinos 789, Las Condes","2021-11-05","2022-11-05"],
            ["10396020-7","Luis","Martínez","Licencia Clase B","Camino Real 321, Ñuñoa","2022-08-22","2023-08-22"],
        ]

        #Aqui tengo mis datos de prueba los traje de una lista que me habia hecho en .txt
        datos_prueba_pasajero = [
            # Formato: rut, nombre, apellido, telefono, empresa
            ["24646811-7", "PFTESTUNO", "TEST", "+56900000001", "Falabella","Plaza de maipu"],
            ["23458382-4", "PFTESTDOS", "TEST", "+56900000002", "Falabella","Plaza de maipu"],
            ["16369291-0", "PFTESTTRES", "TEST", "+56900000003", "FalaBella","Los Héroes"],
            ["21774266-8", "PFTESTCUATRO", "TEST", "+56900000004", "FALABELLA","Puente Cal y Canto"],
            ["10408365-k", "PATESTCINCO", "TEST", "+56900000005", "ABCDIN","Metro Tobalaba"],
            ["10241599-k", "PATESTSEIS", "TEST", "+56900000006", "ABCDIN","Puente Cal y Canto"],
            ["20531884-4", "PFTESTSIETE", "TEST", "+56900000007", "falabella","Plaza de maipu"],
            ["12759669-7", "Ricardo", "Osorio", "+56908635608", "abcdin","Los Héroes"],
            ["22701744-9", "PedRo", "Urrutia", "+56903040876", "FalaBella","Plaza de maipu"],
            ["17321865-6", "Manuel", "Rosales", "+56934675009", "París","Plaza de maipu"],
            ["24381454-5", "Sabrina", "Fuentes", "+56939000118", "Hites","metro las rejas"],
            ["21249809-2", "Jordan", "Veintitres", "+56987400067", "LaPolar","metro las rejas"],
            ["23775964-8", "GabRiel", "Cortez", "+56904302145", "HITES","Plaza de maipu"],
            ["20419312-6", "Paulina", "Bustamante", "+56987320022", "Falabella","Metro Tobalaba"],
            ["10819855-9", "alonso", "Fuentes", "+56923508934", "paris","Metro Tobalaba"],
            ["20183418-k", "nicolas", "Vera", "+56920407733", "PARIS","metro las rejas"],
            ["19099072-9", "Byron", "rebolledo", "+56910893675", "LAPOLAR","Plaza Egaña"],
            ["9198958-1", "Francisco", "torres", "+56934067008", "MANUFACTURAS LOUIS PHILLIPE","Plaza de maipu"],
            ["20704032-0", "Fabian", "Duarte", "+56934011023", "hITES","Plaza de maipu"],
            ["12866940-k", "Shur", "Montecarlo", "+56956400199", "FAlaBella","Plaza de maipu"],
            ["20780883-0", "Vicente", "Díaz", "+56970231991", "Rhode Island","Plaza de maipu"],
            ["6792098-8", "Sebastián", "Mendoza", "+569300022204", "RhodeIsland","Plaza de maipu"],
            ["12467690-8", "Sergio", "Muñoz", "+56941098067", "Rhode Island","Plaza de maipu"],
            ["14924226-0", "Sarah", "Kerrigan", "+56900172355", "PCFACTORY","Plaza de maipu"],
            ["22402627-7", "Alejandra", "Schifer", "+56998007042", "PCFACTORY","Plaza de maipu"],
            ["13304874-k", "Marisol", "Alba", "+56914112051", "Pcfactory","Plaza de maipu"],
            ["21927255-3", "Iván", "Soto", "+56900200025", "Pcfactory","Plaza de maipu"],
            ["20858239-9", "Eduardo", "Alvarez", "+56911097033", "Enea","Plaza de maipu"],
            ["6580174-4", "Pablo", "Inostroza", "+56945012225", "ENEA","Metro Tobalaba"],
            ["18754185-9", "Santiago", "Poblete", "+56912309808", "eNEA","Metro Tobalaba"],
            ["17120537-9", "Adrián", "Ibañez", "+56907702443", "aBCDIN","Metro Tobalaba"],
            ["15678415-k", "Patricio", "Rojas", "+56952319908", "pARIS","Plaza de maipu"],
            ["7477057-6", "Gonzalo", "Montserrat", "+56988430008", "París","Estación Central"],
            ["8711433-3", "María", "Rosende", "+56976984412", "abcdin","Estación Central"],
            ["24098944-1", "Felipe", "Rojas", "+56943021166", "Manufacturas ElBigotes","Plaza Egaña"],
            ["23824638-5", "Roberto", "Mora", "+56915302034", "Manufacturas Louis Phillipe","Plaza de maipu"],
            ["23982034-4", "Daniela", "Alba", "+56988052011", "Manufacturas ElBigotes","Plaza Egaña"],
           
        ]
        
       #Crear paraderos de prueba
        for dato_prueba in datos_prueba_paraderos:
            nombre, tipo_parada, direccion, latitud, longitud = dato_prueba
            Parada.objects.create(
                nombre=nombre,
                tipo_parada=tipo_parada,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud
            )
            paraderos_creados +=1
        self.stdout.write(self.style.SUCCESS(f"Creados {paraderos_creados} paraderos de prueba."))
        
        #Crear vehiculos de prueba
        for dato_prueba in datos_prueba_vehiculos:
            patente, marca, modelo, anio, capacidad, estado, revision_tecnica, proxima_revision = dato_prueba
            Vehiculo.objects.create(
                patente=patente,
                marca=marca,
                modelo=modelo,
                anio=anio,
                capacidad=capacidad,
                estado=estado,
                revision_tecnica=revision_tecnica,
                proxima_revision=proxima_revision
            )
            vehiculos_creados +=1
        self.stdout.write(self.style.SUCCESS(f"Creados {vehiculos_creados} vehículos de prueba."))

        #Crear choferes de prueba
        for dato_prueba in datos_prueba_choferes:
            rut, nombre, apellido, tipo_licencia, direccion, fecha_ultimo_control, fecha_proximo_control = dato_prueba
            Chofer.objects.create(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                tipo_licencia=tipo_licencia,
                direccion=direccion,
                fecha_ultimo_control=fecha_ultimo_control,
                fecha_proximo_control=fecha_proximo_control
            )
            choferes_creados +=1
        self.stdout.write(self.style.SUCCESS(f"Creados {choferes_creados} choferes de prueba."))

        #Creo un pasajero
        for dato_prueba in datos_prueba_pasajero:
            rut, nombre, apellido, telefono, empresa_trabajo, paradero_deseado = dato_prueba
            
            parada = Parada.objects.filter(nombre=paradero_deseado)
            if parada.exists():
                parada = parada.first()
            else:
                parada  = Parada.objects.create(nombre=paradero_deseado, tipo_parada="Desconocido", direccion="Desconocida", latitud=0.0, longitud=0.0)
            
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
                        empresa_trabajo=empresa_trabajo,
                        paradero_deseado=parada
                    )
                pasajeros_creados += 1
                self.stdout.write(f"Creado pasajero: {nombre} {apellido} ({rut})")
        self.stdout.write(self.style.SUCCESS(f"Procesamiento completado: {pasajeros_creados} pasajeros creados, {pasajeros_existentes} omitidos"))
