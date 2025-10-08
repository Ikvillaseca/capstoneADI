import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_direccion

class TestValidarDireccion(unittest.TestCase):
    def test_direccion_Valida(self):
        resultado = validar_direccion("Calle Falsa 123")
        self.assertEqual(resultado, "Calle Falsa 123")
    
    def test_direccion_corta(self):
        with self.assertRaises(Exception) as context:
            validar_direccion("Cal") 
        self.assertTrue("La dirección debe tener al menos 5 caracteres." in str(context.exception))



if __name__ == '__main__':
    unittest.main()
