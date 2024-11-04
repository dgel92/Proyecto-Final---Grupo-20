from src.conn.db_conn import connect_to_mysql
from datetime import datetime


def comprar_accion(cuit, simbolo, cantidad):
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            # Lógica para verificar si el usuario tiene saldo suficiente
            cursor.execute("SELECT saldo FROM inversores WHERE cuit = %s", (cuit,))
            saldo = cursor.fetchone()[0]

            # Suponiendo que tienes una función que obtiene el precio de la acción
            precio_accion = obtener_precio_accion(simbolo)
            costo_total = precio_accion * cantidad

            if saldo >= costo_total:
                # Realizar la compra
                cursor.execute(
                    "INSERT INTO transacciones (cuit_inversor, simbolo, cantidad, precio) VALUES (%s, %s, %s, %s)",
                    (cuit, simbolo, cantidad, precio_accion),
                )
                # Actualizar el saldo
                nuevo_saldo = saldo - costo_total
                cursor.execute(
                    "UPDATE inversores SET saldo = %s WHERE cuit = %s",
                    (nuevo_saldo, cuit),
                )
                connection.commit()
                print("Compra realizada con éxito.")
            else:
                print("Saldo insuficiente para realizar la compra.")
        except mysql.connector.Error as err:
            print(f"Error al realizar la compra: {err}")
        finally:
            cursor.close()
            connection.close()


def vender_accion(inversor_id, simbolo, cantidad):
    connection = connect_to_mysql()
    if connection and connection.is_connected():
        cursor = connection.cursor(dictionary=True)
        try:
            if cantidad <= 0:
                print("La cantidad debe ser un número positivo.")
                return

            # Verificar si el inversor tiene suficientes acciones
            cursor.execute(
                "SELECT cantidad FROM portafolio WHERE inversor_id = %s AND simbolo = %s",
                (inversor_id, simbolo),
            )
            resultado = cursor.fetchone()
            if not resultado or resultado["cantidad"] < cantidad:
                print("No tienes suficientes acciones para vender.")
                return

            cursor.execute(
                "INSERT INTO transacciones (inversor_id, simbolo, tipo, cantidad) VALUES (%s, %s, 'venta', %s)",
                (inversor_id, simbolo, cantidad),
            )
            connection.commit()
            print("Venta realizada con éxito.")
        except Exception as e:
            print(f"Error al realizar la venta: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos")


def calcular_rendimiento(inversor_id, fecha_inicio, fecha_fin):
    connection = connect_to_mysql()
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            # Validar fechas
            datetime.strptime(fecha_inicio, "%Y-%m-%d")
            datetime.strptime(fecha_fin, "%Y-%m-%d")

            if fecha_inicio >= fecha_fin:
                print("La fecha de inicio debe ser anterior a la fecha de fin.")
                return

            cursor.execute(
                """
                SELECT SUM(precio_final - precio_inicial) AS rendimiento
                FROM transacciones
                WHERE inversor_id = %s AND fecha BETWEEN %s AND %s
                """,
                (inversor_id, fecha_inicio, fecha_fin),
            )
            resultado = cursor.fetchone()
            rendimiento = resultado[0] if resultado[0] is not None else 0
            print(
                f"El rendimiento entre {fecha_inicio} y {fecha_fin} es: {rendimiento}"
            )
        except Exception as e:
            print(f"Error al calcular el rendimiento: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos")


def menu_principal(inversor_id):
    while True:
        print("\n--- Panel de Control ---")
        print("1. Comprar Acción")
        print("2. Vender Acción")
        print("3. Calcular Rendimiento")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            simbolo = input("Ingrese el símbolo de la acción: ")
            try:
                cantidad = int(input("Ingrese la cantidad de acciones a comprar: "))
                comprar_accion(inversor_id, simbolo, cantidad)
            except ValueError:
                print("Por favor, ingrese un número válido para la cantidad.")
        elif opcion == "2":
            simbolo = input("Ingrese el símbolo de la acción: ")
            try:
                cantidad = int(input("Ingrese la cantidad de acciones a vender: "))
                vender_accion(inversor_id, simbolo, cantidad)
            except ValueError:
                print("Por favor, ingrese un número válido para la cantidad.")
        elif opcion == "3":
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            calcular_rendimiento(inversor_id, fecha_inicio, fecha_fin)
        elif opcion == "4":
            print("Saliendo del panel de control.")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    inversor_id = input("Ingrese su ID de inversor: ")
    menu_principal(inversor_id)
