import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_nombre_paradero

# Clase de prueba unitaria para la función validar_nombre_paradero debido a que los paraderos pueden tener tanto letras como numeros en su nombre en su nombre

class TestValidarNombreParadero(unittest.TestCase):
    def test_nombre_valido_letras(self):
        resultado = validar_nombre_paradero("Paradero Central")
        self.assertEqual(resultado, "Paradero Central")

    def test_nombre_valido_numeros(self):
        resultado = validar_nombre_paradero("Paradero 123")
        self.assertEqual(resultado, "Paradero 123")
    
    def test_nombre_valido_mixto(self):
        resultado = validar_nombre_paradero("Paradero A1")
        self.assertEqual(resultado, "Paradero A1")

    # Caso de prueba para nombre de paraderos inválido 
    def test_nombre_invalido_vacio(self):
        with self.assertRaises(Exception) as context:
            validar_nombre_paradero("")
        self.assertTrue("El nombre es obligatorio." in str(context.exception))

    def test_nombre_invalido_muy_corto(self):
        with self.assertRaises(Exception) as context:
            validar_nombre_paradero("AB")
        self.assertIn("al menos 3 caracteres", str(context.exception))

    def test_nombre_invalido_muy_largo(self):
        nombre_largo = "A" * 50  
        with self.assertRaises(Exception) as context:
            validar_nombre_paradero(nombre_largo)
        self.assertIn("más de 45 caracteres", str(context.exception))





if __name__ == '__main__':
    unittest.main()
