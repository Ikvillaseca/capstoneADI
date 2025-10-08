import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_telefono

class TestValidarPasajeroTelefono(unittest.TestCase):
    #Telefonos validos
    def test_telefono_formato_internacional(self):
        resultado = validar_telefono("+56954290220")
        self.assertEqual(resultado, "+56954290220")
    
    def test_telefono_formato_nacional(self):
        resultado = validar_telefono("954290220")
        self.assertEqual(resultado, "+56954290220")
    
    def test_telefono_internacional(self):
        resultado = validar_telefono("+51912345678")
        self.assertEqual(resultado, "+51912345678")
    
    #Telefonos invalidos
    def test_telefono_invalido_con_espacio(self):
        with self.assertRaises(Exception) as context:
            validar_telefono("+569 5429 0220")
        self.assertTrue("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)" in str(context.exception))

    def test_telefono_invalido_con_letras(self):
        with self.assertRaises(Exception) as context:
            validar_telefono("+5695e290220")
        self.assertTrue("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)" in str(context.exception))

    def test_telefono_invalido_sin_mas(self):
        with self.assertRaises(Exception) as context:
            validar_telefono("56954290220")
        self.assertTrue("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)" in str(context.exception))

    def test_telefono_invalido_corto(self):
        with self.assertRaises(Exception) as context:
            validar_telefono("+5695429")
        self.assertTrue("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)" in str(context.exception))

    def test_telefono_invalido_largo(self):
        with self.assertRaises(Exception) as context:
            validar_telefono("+56954293284573248905")
        self.assertTrue("El teléfono debe tener un formato válido (ej: +56912345678 o 912345678 para Chile, o formato internacional como +51912345678)" in str(context.exception))

if __name__ == '__main__':
    unittest.main()
