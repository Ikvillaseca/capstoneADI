import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_rut
from RouteAnvil.models import Chofer, Pasajero

class TestValidarRut(unittest.TestCase):
    def test_rut_valido(self):
        resultado = validar_rut("20534144-7",Chofer, None)
        self.assertEqual(resultado, "20534144-7")




if __name__ == '__main__':
    unittest.main()
