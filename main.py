import sys
import signal
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from gestor import GestorBD
from servidor import ServidorREST

def main():
    print("=== Servidor de Base de Datos ===")
    
    # Verificar que exista el .env
    if not os.path.exists('.env'):
        print("Error: Archivo .env no encontrado")
        print("   Crea el archivo .env con tu DATABASE_URL")
        sys.exit(1)
    
    # Verificar DATABASE_URL
    if not Config.DATABASE_URL:
        print("Error: DATABASE_URL no configurada en .env")
        sys.exit(1)
    
    print("Conectando a la base de datos...")
    
    # Conectar a MySQL (sin ssl_ca_path)
    gestor_bd = GestorBD(Config.DATABASE_URL)
    
    # Probar conexión
    if not gestor_bd.probar_conexion():
        print("No se pudo conectar a la base de datos")
        print("Verifica tus credenciales en el archivo .env")
        sys.exit(1)
    
    # Crear tablas
    try:
        gestor_bd.crear_tablas()
        print("Tablas creadas/verificadas correctamente")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        sys.exit(1)
    
    # Iniciar servidor
    servidor = ServidorREST(
        host=Config.SERVER_HOST,
        puerto=Config.SERVER_PORT,
        gestor_bd=gestor_bd
    )
    
    def signal_handler(sig, frame):
        print("\nDeteniendo servidor...")
        servidor.detener()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Servidor en http://{Config.SERVER_HOST}:{Config.SERVER_PORT}")
    print("Presiona Ctrl+C para detener")
    servidor.iniciar()

if __name__ == "__main__":
    main()