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

    def test_rut_invalido_formato(self):
        with self.assertRaises(Exception) as context:
            validar_rut("205341447",Chofer, None)
        self.assertTrue("El RUT debe tener el siguiente formato (ejemplo: 12345678-9)." in str(context.exception))
        
    def test_rut_invalido_dv(self):
        with self.assertRaises(Exception) as context:
            validar_rut("20534144-8",Chofer, None)
        self.assertTrue("El RUT ingresado no es válido. Verifique el dígito verificador." in str(context.exception))

    # Pruebas adicionales con digito verificador '0' y 'k'
    def test_rut_0(self):
        resultado = validar_rut("6124839-0", Pasajero, None)
        self.assertEqual(resultado, "6124839-0")

    def test_rut_k(self):
        resultado = validar_rut("13065360-k", Chofer, None)
        self.assertEqual(resultado, "13065360-k")
    






if __name__ == '__main__':
    unittest.main()
