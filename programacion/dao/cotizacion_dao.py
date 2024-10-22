import sys
import os

# Añadir el directorio base del proyecto al sys.path para resolver las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conn.conn_db import conectar_bd
from models.cotizacion import Cotizacion

class CotizacionDAO:
    def __init__(self):
        self.conn = conectar_bd()

    def registrar_cotizacion(self, codigo_accion, precio):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cotizaciones (codigo_accion, precio, fecha)
                VALUES (%s, %s, NOW())
            """, (codigo_accion, precio))
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error al registrar la cotización: {}".format(err))
        finally:
            cursor.close()

    def obtener_cotizaciones_por_codigo(self, codigo_accion):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cotizaciones WHERE codigo_accion = %s", (codigo_accion,))
        cotizaciones = cursor.fetchall()
        cursor.close()
        return cotizaciones

    def cerrar_conexion(self):
        self.conn.close()

# Pruebas de ejemplo
if __name__ == "__main__":
    cotizacion_dao = CotizacionDAO()

    # Registrar una cotización de prueba
    cotizacion_dao.registrar_cotizacion('AAPL', 150.25)

    # Obtener cotizaciones por código de acción
    cotizaciones = cotizacion_dao.obtener_cotizaciones_por_codigo('AAPL')
    for cotizacion in cotizaciones:
        print(cotizacion)
    
    # Cerrar la conexión a la base de datos
    cotizacion_dao.cerrar_conexion()
