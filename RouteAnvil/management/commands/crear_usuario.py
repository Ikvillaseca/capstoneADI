from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import CustomUser
from RouteAnvil.models import Chofer
import uuid

class Command(BaseCommand):
    help = 'Crea usuarios de forma interactiva (Administradores o Choferes)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tipo',
            type=str,
            choices=['admin', 'chofer'],
            help='Tipo de usuario: admin o chofer'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email del usuario'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Contraseña del usuario'
        )
        parser.add_argument(
            '--nombre',
            type=str,
            help='Nombre del usuario'
        )
        parser.add_argument(
            '--apellido',
            type=str,
            help='Apellido del usuario'
        )
        parser.add_argument(
            '--chofer-id',
            type=str,
            help='ID del chofer existente (solo para tipo chofer)'
        )

    def handle(self, *args, **options):
        # Verificar que existan los grupos
        try:
            grupo_admin = Group.objects.get(name='Administradores')
        except Group.DoesNotExist:
            grupo_admin = Group.objects.create(name='Administradores')
            self.stdout.write(self.style.WARNING('Grupo Administradores creado'))
        
        try:
            grupo_chofer = Group.objects.get(name='Choferes')
        except Group.DoesNotExist:
            grupo_chofer = Group.objects.create(name='Choferes')
            self.stdout.write(self.style.WARNING('Grupo Choferes creado'))

        # Si se pasaron argumentos, usar esos
        if options['tipo'] and options['email'] and options['password']:
            self.crear_usuario_con_args(options, grupo_admin, grupo_chofer)
        else:
            # Modo interactivo
            self.crear_usuario_interactivo(grupo_admin, grupo_chofer)

    def crear_usuario_con_args(self, options, grupo_admin, grupo_chofer):
        """Crea usuario usando argumentos de línea de comando"""
        tipo = options['tipo']
        email = options['email']
        password = options['password']
        nombre = options.get('nombre', '')
        apellido = options.get('apellido', '')
        chofer_id = options.get('chofer_id')

        try:
            # Verificar si el email ya existe
            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f'El email {email} ya está en uso'))
                return

            # Crear usuario
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
                is_email_verified=True
            )

            if tipo == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
                user.groups.add(grupo_admin)
                self.stdout.write(self.style.SUCCESS(
                    f'Usuario Administrador creado exitosamente'
                ))
                self.stdout.write(f'  Email: {email}')
                self.stdout.write(f'  Contraseña: ****')
            
            elif tipo == 'chofer':
                user.groups.add(grupo_chofer)
                
                # Si se proporcionó un ID de chofer, vincular
                if chofer_id:
                    try:
                        chofer_uuid = uuid.UUID(chofer_id)
                        chofer = Chofer.objects.get(id_chofer=chofer_uuid)
                        chofer.user = user
                        chofer.save()
                        self.stdout.write(self.style.SUCCESS(
                            f'Usuario Chofer creado y vinculado exitosamente'
                        ))
                        self.stdout.write(f'  Chofer: {chofer.nombre} {chofer.apellido}')
                    except Chofer.DoesNotExist:
                        self.stdout.write(self.style.ERROR(
                            f'No se encontró chofer con ID {chofer_id}'
                        ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f'Usuario Chofer creado exitosamente'
                    ))
                
                self.stdout.write(f'  Email: {email}')
                self.stdout.write(f'  Contraseña: ****')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear usuario: {str(e)}'))

    def crear_usuario_interactivo(self, grupo_admin, grupo_chofer):
        """Crea usuario de forma interactiva"""
        self.stdout.write(self.style.SUCCESS('\n=== Creación de Usuario ===\n'))

        # Seleccionar tipo de usuario
        self.stdout.write('Tipo de usuario:')
        self.stdout.write('  1. Administrador')
        self.stdout.write('  2. Chofer')
        tipo_input = input('\nSeleccione opción (1 o 2): ').strip()

        if tipo_input not in ['1', '2']:
            self.stdout.write(self.style.ERROR('Opción inválida'))
            return

        es_admin = tipo_input == '1'

        # Obtener datos del usuario
        email = input('\nEmail: ').strip()
        
        # Verificar si el email ya existe
        if CustomUser.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'El email {email} ya está en uso'))
            return

        password = input('Contraseña: ').strip()
        nombre = input('Nombre: ').strip()
        apellido = input('Apellido: ').strip()

        try:
            # Crear usuario
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
                is_email_verified=True
            )

            if es_admin:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                user.groups.add(grupo_admin)
                self.stdout.write(self.style.SUCCESS('\nUsuario Administrador creado exitosamente'))
            else:
                user.groups.add(grupo_chofer)
                
                # Preguntar si vincular con chofer existente
                vincular = input('\n¿Vincular con chofer existente? (s/n): ').strip().lower()
                
                if vincular == 's':
                    # Mostrar choferes disponibles sin usuario
                    choferes_disponibles = Chofer.objects.filter(user__isnull=True)
                    
                    if choferes_disponibles.exists():
                        self.stdout.write('\nChoferes disponibles:')
                        for chofer in choferes_disponibles:
                            self.stdout.write(
                                f'  ID: {chofer.id_chofer} - {chofer.nombre} {chofer.apellido} (RUT: {chofer.rut})'
                            )
                        
                        chofer_id_input = input('\nIngrese ID del chofer: ').strip()
                        
                        try:
                            chofer_uuid = uuid.UUID(chofer_id_input)
                            chofer = Chofer.objects.get(id_chofer=chofer_uuid)
                            chofer.user = user
                            chofer.save()
                            self.stdout.write(self.style.SUCCESS(
                                f'Usuario vinculado con chofer {chofer.nombre} {chofer.apellido}'
                            ))
                        except (Chofer.DoesNotExist, ValueError):
                            self.stdout.write(self.style.WARNING(
                                'No se pudo vincular con el chofer'
                            ))
                    else:
                        self.stdout.write(self.style.WARNING(
                            'No hay choferes disponibles sin usuario'
                        ))
                
                self.stdout.write(self.style.SUCCESS('\nUsuario Chofer creado exitosamente'))

            # Mostrar resumen
            self.stdout.write('\n' + '='*50)
            self.stdout.write('RESUMEN DEL USUARIO CREADO')
            self.stdout.write('='*50)
            self.stdout.write(f'Email: {email}')
            self.stdout.write(f'Nombre: {nombre} {apellido}')
            self.stdout.write(f'Tipo: {"Administrador" if es_admin else "Chofer"}')
            self.stdout.write(f'Grupos: {", ".join(user.groups.values_list("name", flat=True))}')
            if hasattr(user, 'chofer'):
                self.stdout.write(f'Chofer vinculado: {user.chofer.nombre} {user.chofer.apellido}')
            self.stdout.write('='*50)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nError al crear usuario: {str(e)}'))