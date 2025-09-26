from behave.__main__ import main as behave_main
from django.core import management
import os
import sys
import time
import webbrowser
import subprocess

def run_tests():
    #Obtener la ubicacion actual
    ubicacion_actual = os.path.dirname(os.path.abspath(__file__))
    os.chdir(ubicacion_actual)

    #Activo el modo test
    env = os.environ.copy()
    env['test'] = 'true'
    #Migro la base de datos
    server_setup_cmd = [sys.executable, '../manage.py', 'migrate']
    subprocess.Popen(server_setup_cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE).wait()

        
    #Corro la pagina de django
    server_cmd = [sys.executable, '../manage.py', 'runserver']
    proceso_server_pruebas = subprocess.Popen(server_cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)


    time.sleep(2) #Esperar que ejecute el runserver
    #Correr las pruebas con behave basado en behave -f html -o behave-report.html
    sys.argv = [
        'behave',
        '--no-capture',
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

    #Cerrar el servidor luego de la ejecucion
    if proceso_server_pruebas:
        print("Cerrando servidor Django...")
        subprocess.Popen("TASKKILL /F /PID {} /T".format(proceso_server_pruebas.pid)).wait()
        
    #Limpiar base de datos de Django de pruebas
    eleccion = input("Desea eliminar la base de datos de prueba? S/N:\n")
    if eleccion == "S":
        os.remove(os.path.join(os.getcwd(), "../db-test.sqlite3")) 
    env['test'] = 'false'
    

if __name__ == '__main__':
    run_tests()