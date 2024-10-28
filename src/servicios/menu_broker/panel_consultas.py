from src.conn.db_conn import connect_to_mysql
from datetime import datetime


def comprar_accion(inversor_id, simbolo, cantidad):
    connection = connect_to_mysql()
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            # Validación de cantidad
            if cantidad <= 0:
                print("La cantidad debe ser un número positivo.")
                return

            cursor.execute(
                "INSERT INTO transacciones (inversor_id, simbolo, tipo, cantidad) VALUES (%s, %s, 'compra', %s)",
                (inversor_id, simbolo, cantidad),
            )
            connection.commit()
            print("Compra realizada con éxito.")
        except Exception as e:
            print(f"Error al realizar la compra: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos")


def vender_accion(inversor_id, simbolo, cantidad):
    connection = connect_to_mysql()
    if connection and connection.is_connected():
        cursor = connection.cursor()
        try:
            if cantidad <= 0:
                print("La cantidad debe ser un número positivo.")
                return

            # Aquí podrías agregar una verificación para ver si el inversor tiene suficientes acciones

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
