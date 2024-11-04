import bcrypt
import mysql.connector  # Asegúrate de importar este módulo
from src.conn.db_conn import connect_to_mysql
from src.servicios.broker.menu_broker import menu_principal


def registrar_usuario(nombre, email, password):
    connection = connect_to_mysql()
    if connection:
        cursor = connection.cursor()
        try:
            # Verificar si el email ya está registrado
            cursor.execute("SELECT email FROM inversores WHERE email = %s", (email,))
            if cursor.fetchone():
                print("El email ingresado ya está registrado.")
                return

            # Hash de la contraseña
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Insertar el nuevo usuario sin intentos_fallidos ni bloqueado
            cursor.execute(
                "INSERT INTO inversores (nombre, email, contraseña) VALUES (%s, %s, %s)",
                (nombre, email, hashed_password),
            )
            connection.commit()
            print("Usuario registrado con éxito.")

            # Obtener el ID del inversor para pasar al menú
            cursor.execute("SELECT cuit FROM inversores WHERE email = %s", (email,))
            inversor_id = cursor.fetchone()[0]
            menu_principal(inversor_id)  # Llamar al menú broker
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("No se pudo conectar a la base de datos.")


def iniciar_sesion(email, password):
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM inversores WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if not usuario:
                print("Error: El email ingresado no está registrado.")
                return False

            if bcrypt.checkpw(
                password.encode("utf-8"), usuario["contraseña"].encode("utf-8")
            ):
                print(f"Bienvenido {usuario['nombre']}!")
                menu_principal(usuario["cuit"])  # Usar cuit como ID
                return True
            else:
                print("Contraseña incorrecta.")
                return False
    except mysql.connector.Error as err:
        print(f"Error al iniciar sesión: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()


def recuperar_contrasena(email, nueva_password):
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(
                nueva_password.encode("utf-8"), bcrypt.gensalt()
            )
            cursor.execute(
                "UPDATE inversores SET contraseña = %s WHERE email = %s",
                (hashed_password, email),
            )
            connection.commit()
            print("Contraseña actualizada con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al actualizar la contraseña: {err}")
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    print("1. Registrar Usuario")
    print("2. Iniciar Sesión")
    print("3. Recuperar Contraseña")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Ingrese su nombre: ")
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")
        registrar_usuario(nombre, email, password)
    elif opcion == "2":
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")
        iniciar_sesion(email, password)
    elif opcion == "3":
        email = input("Ingrese su email: ")
        nueva_password = input("Ingrese su nueva contraseña: ")
        recuperar_contrasena(email, nueva_password)
    else:
        print("Opción no válida.")
