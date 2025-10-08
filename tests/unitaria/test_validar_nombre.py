import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_texto


class TestValidarNombre(unittest.TestCase):
    def test_nombre(self):
        resultado = validar_texto("Jorge")
        self.assertEqual(resultado, "Jorge")
    
    def test_nombre_con_espacio(self):
        with self.assertRaises(Exception) as context:
            validar_texto("Jorge Luis")
        self.assertTrue("El texto solo debe contener letras." in str(context.exception))

    def test_nombre_con_numero(self):
        with self.assertRaises(Exception) as context:
            validar_texto("12345")
        self.assertTrue("El texto solo debe contener letras." in str(context.exception))




if __name__ == '__main__':
    unittest.main()
