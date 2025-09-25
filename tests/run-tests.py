from behave.__main__ import main as behave_main
import sys
import time
import webbrowser
import os

#Obtener la ubicacion actual y ejecutar el comando "behave -f html -o ./behave-report.html"
ubicacion_actual = os.path.dirname(os.path.abspath(__file__))
os.chdir(ubicacion_actual)
sys.argv = [
    'behave',
    '-f', 'html',
    '-o', './behave-report.html'
]
behave_main()

#Obtener la ubicacion del reporte y abrirlo usando el navegador
ubicacion_reporte = os.path.join(os.getcwd(), "behave-report.html")
try:
    archivo_url = f"file:///{ubicacion_reporte.replace(os.sep, '/')}"
    print(f"\n Abriendo reporte de pruebas: {archivo_url}")
    # Esperar un momento para que el reporte se genere completamente
    time.sleep(2)
    webbrowser.open(archivo_url, new=2)
except:
    print("No se encontró el archivo")

input("Presione Enter para cerrar...")