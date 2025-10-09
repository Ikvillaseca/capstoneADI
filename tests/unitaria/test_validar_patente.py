import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_patente

class TestValidarPatente(unittest.TestCase):
    def test_patente_valida(self):
        resultado = validar_patente("ABCD12")
        self.assertEqual(resultado, "ABCD12")

    def test_patente_valida_formato2(self):
        resultado = validar_patente("AB1234")
        self.assertEqual(resultado, "AB1234")

    #Patentes inválidas
    def test_patente_invalida(self):
        with self.assertRaises(Exception) as context:
            validar_patente("123456")
        self.assertTrue("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12)." in str(context.exception))
    
    def test_patente_formato_invalido(self):
        with self.assertRaises(Exception) as context:
            validar_patente("A1B2C3")
        self.assertTrue("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12)." in str(context.exception))

    def test_patente_minuscula(self):
        with self.assertRaises(Exception) as context:
            validar_patente("abcd12")
        self.assertTrue("La patente debe ser en mayúsculas y debe tener uno de los siguientes formatos (ejemplo: AB1234 o ABCD12)." in str(context.exception))

if __name__ == '__main__':
    unittest.main()