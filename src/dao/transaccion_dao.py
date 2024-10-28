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
            cursor.execute(
                "UPDATE acciones SET cantidad_disponible = %s WHERE codigo = %s",
                (cantidad, codigo),
            )
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error al actualizar la cantidad de acciones: {}".format(err))
        finally:
            cursor.close()

    def obtener_todas(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM acciones")
        acciones = cursor.fetchall()
        cursor.close()
        return acciones

    def cerrar_conexion(self):
        self.conn.close()


class InversorDAO:
    def __init__(self):
        self.conn = conectar_bd()

    def obtener_por_email(self, email):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inversores WHERE email = %s", (email,))
        inversor = cursor.fetchone()
        cursor.close()
        return inversor

    def actualizar_saldo(self, cuit, nuevo_saldo):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "UPDATE inversores SET saldo = %s WHERE cuit = %s", (nuevo_saldo, cuit)
            )
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error al actualizar el saldo del inversor: {}".format(err))
        finally:
            cursor.close()

    def cerrar_conexion(self):
        self.conn.close()


def comprar_accion(inversor_email, codigo_accion, cantidad):
    inversor_dao = InversorDAO()
    accion_dao = AccionDAO()

    inversor = inversor_dao.obtener_por_email(inversor_email)
    if not inversor:
        print("Inversor no encontrado.")
        return

    accion = accion_dao.obtener_por_codigo(codigo_accion)
    if not accion:
        print("Acción no disponible en el mercado.")
        return

    total_compra = accion["precio_compra"] * cantidad
    comision = total_compra * 0.01  # Comisión del 1%
    total_con_comision = total_compra + comision

    if inversor["saldo"] < total_con_comision:
        print("Saldo insuficiente para realizar la compra.")
        return

    nuevo_saldo = inversor["saldo"] - total_con_comision
    nueva_cantidad_disponible = accion["cantidad_disponible"] - cantidad

    if nueva_cantidad_disponible < 0:
        print("No hay suficientes acciones disponibles en el mercado.")
        return

    # Registrar la transacción
    cursor = accion_dao.conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO transacciones (cuit, codigo_accion, tipo, cantidad, precio, total, fecha)
            VALUES (%s, %s, 'compra', %s, %s, %s, NOW())
        """,
            (
                inversor["cuit"],
                codigo_accion,
                cantidad,
                accion["precio_compra"],
                total_con_comision,
            ),
        )
        accion_dao.conn.commit()
    except mysql.connector.Error as err:
        print("Error al registrar la transacción: {}".format(err))
    finally:
        cursor.close()

    # Actualizar la cantidad de acciones disponibles
    accion_dao.actualizar_cantidad(codigo_accion, nueva_cantidad_disponible)

    # Actualizar el saldo del inversor
    inversor_dao.actualizar_saldo(inversor["cuit"], nuevo_saldo)

    print(f"Compra de {cantidad} acciones de {codigo_accion} realizada con éxito.")

    # Cerrar las conexiones
    inversor_dao.cerrar_conexion()
    accion_dao.cerrar_conexion()


# Pruebas de ejemplo
if __name__ == "__main__":
    # Obtener información de una acción
    accion_dao = AccionDAO()
    accion = accion_dao.obtener_por_codigo("AAPL")
    print(accion)

    # Actualizar la cantidad disponible de una acción
    accion_dao.actualizar_cantidad("AAPL", 1500)

    # Comprar una acción
    comprar_accion("juan.perez@gmail.com", "AAPL", 10)

    # Cerrar la conexión a la base de datos
    accion_dao.cerrar_conexion()
