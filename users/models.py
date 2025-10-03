from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    # En base al modelo de AbstractUser que provee Django:
    # Eliminamos el campo username del modelo base
    username = None
    # Hacemos que el email sea único y el campo para el login
    email = models.EmailField(_('email address'), unique=True)
    
    # Campo para verificar si el correo ha sido validado
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # email y password son requeridos por defecto asi que se deja vacio

    objects = CustomUserManager()

    def __str__(self):
        return self.email