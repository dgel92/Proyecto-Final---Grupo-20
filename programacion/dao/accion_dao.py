from ..conn.conn_db import conectar_bd

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