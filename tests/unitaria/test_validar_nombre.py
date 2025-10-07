import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_nombre
from RouteAnvil.models import Chofer, Pasajero

class TestValidarNombre(unittest.TestCase):
    def test_nombre(self):
        resultado = validar_nombre("Jorge")
        self.assertEqual(resultado, "Jorge")




if __name__ == '__main__':
    unittest.main()
