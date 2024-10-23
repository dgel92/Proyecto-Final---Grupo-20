import sys
import os

# Añadir el directorio base del proyecto al sys.path para resolver las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conn.conn_db import conectar_bd

class AccionDAO:
    def __init__(self):
        self.conn = conectar_bd()

    def obtener_por_codigo(self, codigo):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM acciones WHERE codigo = %s", (codigo,))
        accion = cursor.fetchone()
        cursor.close()
        return accion

    def actualizar_cantidad(self, codigo, cantidad):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE acciones SET cantidad_disponible = %s WHERE codigo = %s", (cantidad, codigo))
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error al actualizar la cantidad de acciones: {}".format(err))
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conn.close()

# Pruebas de ejemplo
if __name__ == "__main__":
    accion_dao = AccionDAO()
    
    # Obtener información de una acción
    accion = accion_dao.obtener_por_codigo('AAPL')
    print(accion)
    
    # Actualizar la cantidad disponible de una acción
    accion_dao.actualizar_cantidad('AAPL', 1500)
    
    # Cerrar la conexión a la base de datos
    accion_dao.cerrar_conexion()

def insertar_accion(codigo, nombre, precio_compra, precio_venta, cantidad_disponible):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO acciones (codigo, nombre, precio_compra, precio_venta, cantidad_disponible)
            VALUES (%s, %s, %s, %s, %s)
        """, (codigo, nombre, precio_compra, precio_venta, cantidad_disponible))
        conn.commit()
        print(f"Acción {nombre} insertada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error al insertar la acción: {err}")
    finally:
        cursor.close()
        conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    # Inserta varias acciones conocidas
    insertar_accion('pepino', 'pepe', 56.80, 57.20, 1000)
