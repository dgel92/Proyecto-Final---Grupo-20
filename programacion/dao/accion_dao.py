from db.conn_db import conectar_bd

class AccionDAO:
    @staticmethod
    def obtener_por_codigo(codigo):
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM acciones WHERE codigo = %s", (codigo,))
        accion = cursor.fetchone()
        cursor.close()
        conn.close()
        return accion

    @staticmethod
    def actualizar_cantidad(codigo, cantidad):
        conn = conectar_bd()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE acciones SET cantidad_disponible = %s WHERE codigo = %s", (cantidad, codigo))
            conn.commit()
        except mysql.connector.Error as err:
            print("Error al actualizar la cantidad de acciones: {}".format(err))
        finally:
            cursor.close()
            conn.close()
