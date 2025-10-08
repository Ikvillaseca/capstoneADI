import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_empresa

class TestValidarPasajeroEmpresa(unittest.TestCase):
    def test_empresa(self):
        resultado = validar_empresa("Fababella")
        self.assertEqual(resultado, "Fababella")
    
    def test_empresa_3_char(self):
        resultado = validar_empresa("CUI")
        self.assertEqual(resultado, "CUI")
    
    def test_empresa_45_char(self):
        resultado = validar_empresa("Lorem ipsum dolor sit amet consectetur adipi.")
        self.assertEqual(resultado, "Lorem ipsum dolor sit amet consectetur adipi.")

    def test_empresa_invalida_corto(self):
        with self.assertRaises(Exception) as context:
            validar_empresa("XD")
        self.assertTrue("El nombre de la empresa debe tener al menos 3 caracteres." in str(context.exception))

    def test_empresa_invalida_largo(self):
        with self.assertRaises(Exception) as context:
            validar_empresa("Lorem ipsum dolor sit amet consectetur adipiscing elit iaculis, potenti vivamus.")
        self.assertTrue("El nombre de la empresa no debe exceder los 45 caracteres." in str(context.exception))




