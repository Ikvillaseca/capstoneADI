import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_capacidad

class TestValidarCapacidad(unittest.TestCase):
    def test_capacidad_valida(self):
        resultado = validar_capacidad("5")
        self.assertEqual(resultado, 5)
 
    # Capacidades inválidas
    def test_capacidad_invalida(self):
        with self.assertRaises(Exception) as context:
            validar_capacidad("c")
        self.assertTrue("La capacidad debe ser un número positivo." in str(context.exception))
         
    def test_capacidad_negativa(self):
        with self.assertRaises(Exception) as context:
            validar_capacidad("-1")
        self.assertTrue("La capacidad debe ser un número positivo." in str(context.exception))
    
    def test_capacidad_decimal(self):
        with self.assertRaises(Exception) as context:
            validar_capacidad("5.5")
        self.assertTrue("La capacidad debe ser un número positivo." in str(context.exception))

if __name__ == '__main__':
    unittest.main()