from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from RouteAnvil.models import Viaje, Pasajero, Chofer, Vehiculo

class Command(BaseCommand):
    help = 'Crea los grupos de usuarios y asigna permisos'

    def handle(self, *args, **options):
        # Crear grupo Administradores/Creadores de Rutas
        admin_group, created = Group.objects.get_or_create(name='Administradores')
        if created:
            # Permisos completos para administradores
            permisos_admin = Permission.objects.filter(
                content_type__model__in=['viaje', 'pasajero', 'chofer', 'vehiculo', 'parada', 'grupo_pasajeros']
            )
            admin_group.permissions.set(permisos_admin)
            self.stdout.write(self.style.SUCCESS('Grupo Administradores creado'))
        
        # Crear grupo Choferes
        chofer_group, created = Group.objects.get_or_create(name='Choferes')
        if created:
            # Permisos limitados para choferes (solo ver viajes)
            viaje_ct = ContentType.objects.get_for_model(Viaje)
            permisos_chofer = Permission.objects.filter(
                content_type=viaje_ct,
                codename__in=['view_viaje']
            )
            chofer_group.permissions.set(permisos_chofer)
            self.stdout.write(self.style.SUCCESS('Grupo Choferes creado'))
        
        self.stdout.write(self.style.SUCCESS('Grupos configurados exitosamente'))