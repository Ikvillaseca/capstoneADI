import unittest #Importamos unittest para realizar las pruebas unitarias
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcapstone.settings')
import django
django.setup()

from RouteAnvil.validadores import validar_fechas_control_medico
from datetime import date, timedelta


class TestValidarFechaControl(unittest.TestCase):
    def test_fechas_validas(self):
        fecha_ultimo = date.today()
        fecha_proximo = fecha_ultimo + timedelta(days=300)
        validar_fechas_control_medico(fecha_ultimo, fecha_proximo)
        self.assertTrue(True) 
    
    def test_fecha_proximo_anterior(self):
        from datetime import date, timedelta
        fecha_ultimo = date.today()
        fecha_proximo = fecha_ultimo - timedelta(days=1)
        with self.assertRaises(Exception) as context:
            validar_fechas_control_medico(fecha_ultimo, fecha_proximo)
        self.assertTrue("La fecha del proximo control debe ser posterior a la del ultimo control." in str(context.exception))

    def test_fecha_proximo_igual(self):
        fecha_ultimo = date.today()
        fecha_proximo = fecha_ultimo
        with self.assertRaises(Exception) as context:
            validar_fechas_control_medico(fecha_ultimo, fecha_proximo)
        self.assertTrue("La fecha del proximo control debe ser posterior a la del ultimo control." in str(context.exception))




if __name__ == '__main__':
    unittest.main()