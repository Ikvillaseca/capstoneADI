import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_anio
from datetime import datetime

class TestValidarAnio(unittest.TestCase):
    def test_anio_valido(self):
        resultado = validar_anio(2020)
        self.assertEqual(resultado, 2020)

    def test_anio_limite_inferior(self):
        resultado = validar_anio(1950)
        self.assertEqual(resultado, 1950)
    
    def test_anio_limite_superior(self):
        resultado = validar_anio(datetime.now().year)
        self.assertEqual(resultado, datetime.now().year)
 
    # Caso de prueba para año inválido 
    def test_anio_invalido_bajo(self):
        with self.assertRaises(Exception) as context:
            validar_anio(1949)
        self.assertTrue("El año debe estar entre 1950 y el año actual." in str(context.exception))

    def test_anio_invalido_alto(self):
        with self.assertRaises(Exception) as context:
            validar_anio(datetime.now().year + 1)
        self.assertTrue("El año debe estar entre 1950 y el año actual." in str(context.exception))


if __name__ == '__main__':
    unittest.main()