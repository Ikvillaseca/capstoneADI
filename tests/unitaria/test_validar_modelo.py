import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_modelo

class TestValidarModelo(unittest.TestCase):
    def test_modelo_valido(self):
        resultado = validar_modelo("Hyundai")
        self.assertEqual(resultado, "Hyundai")

    def test_modelo_3_char(self):
        resultado = validar_modelo("X51")
        self.assertEqual(resultado, "X51")
    
    def test_modelo_45_char(self):
        resultado = validar_modelo("Lorem ipsum dolor sit amet consectetur.")
        self.assertEqual(resultado, "Lorem ipsum dolor sit amet consectetur.")

    # Caso de prueba para modelo inválido 
    def test_modelo_invalido_vacio(self):
        with self.assertRaises(Exception) as context:
            validar_modelo("")
        self.assertTrue("El modelo no puede estar vacío." in str(context.exception))

    def test_modelo_invalido_corto(self):
        with self.assertRaises(Exception) as context:
            validar_modelo("AB")
        self.assertTrue("El modelo debe tener al menos 3 caracteres." in str(context.exception))

    def test_modelo_invalido_largo(self):
        with self.assertRaises(Exception) as context:
            validar_modelo("Lorem ipsum dolor sit amet consectetur adipiscing elit iaculis.")
        self.assertTrue("El modelo no puede exceder los 45 caracteres." in str(context.exception))

if __name__ == '__main__':
    unittest.main()
