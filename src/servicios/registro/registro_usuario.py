from models.usuario import Usuario
from src.conn.db_conn import connect_to_mysql
import bcrypt


def registrar_usuario(usuario):
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor()
            # Verifica si el usuario ya existe
            cursor.execute(
                "SELECT * FROM usuarios WHERE cuil = %s OR email = %s",
                (usuario.cuil, usuario.email),
            )
            if cursor.fetchone():
                print("Error: El CUIL o el email ingresados ya están registrados.")
                return

            # Inserta el nuevo usuario
            query = """
                INSERT INTO usuarios (nombre, apellido, cuil, email, password, pregunta_seguridad, respuesta_seguridad, intentos_fallidos, bloqueado, saldo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                usuario.nombre,
                usuario.apellido,
                usuario.cuil,
                usuario.email,
                usuario.hashed_password,
                usuario.pregunta_seguridad,
                usuario.respuesta_seguridad,
                usuario.intentos_fallidos,
                usuario.bloqueado,
                usuario.saldo,
            )
            cursor.execute(query, values)
            connection.commit()
            print(f"Usuario {usuario.nombre} registrado exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al registrar usuario: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def mostrar_usuarios_registrados():
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            if not usuarios:
                print("No hay usuarios registrados.")
            else:
                for usuario in usuarios:
                    print(f"Email: {usuario['email']}")
                    print(f"Nombre: {usuario['nombre']} {usuario['apellido']}")
                    print(f"CUIL: {usuario['cuil']}")
                    print(f"Saldo: ${usuario['saldo']}")
                    print(f"Bloqueado: {usuario['bloqueado']}")
                    print("-" * 20)
    except mysql.connector.Error as err:
        print(f"Error al mostrar usuarios: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def iniciar_sesion(email, password):
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if not usuario:
                print("Error: El email ingresado no está registrado.")
                return False

            if usuario["bloqueado"]:
                print(
                    "Su cuenta está bloqueada. Debe cambiar la contraseña para poder iniciar sesión."
                )
                return False

            if bcrypt.checkpw(
                password.encode("utf-8"), usuario["password"].encode("utf-8")
            ):
                print(f"Bienvenido {usuario['nombre']}!")
                cursor.execute(
                    "UPDATE usuarios SET intentos_fallidos = %s WHERE email = %s",
                    (0, email),
                )
                connection.commit()
                return True
            else:
                intentos_fallidos = usuario["intentos_fallidos"] + 1
                cursor.execute(
                    "UPDATE usuarios SET intentos_fallidos = %s WHERE email = %s",
                    (intentos_fallidos, email),
                )
                if intentos_fallidos >= 3:
                    cursor.execute(
                        "UPDATE usuarios SET bloqueado = %s WHERE email = %s",
                        (True, email),
                    )
                    print(
                        "Ha superado el número de intentos fallidos. Su cuenta ha sido bloqueada."
                    )
                connection.commit()
                return False
    except mysql.connector.Error as err:
        print(f"Error al iniciar sesión: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def recuperar_contrasena(email, nueva_password, respuesta_seguridad):
    connection = connect_to_mysql()
    try:
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()
            if not usuario:
                print("Error: El email ingresado no está registrado.")
                return

            if usuario["respuesta_seguridad"] != respuesta_seguridad:
                print("Error: Respuesta de seguridad incorrecta.")
                return

            hashed_password = bcrypt.hashpw(
                nueva_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            cursor.execute(
                """
                UPDATE usuarios
                SET password = %s, bloqueado = %s, intentos_fallidos = %s
                WHERE email = %s
            """,
                (hashed_password, False, 0, email),
            )
            connection.commit()
            print("Contraseña actualizada exitosamente y cuenta desbloqueada.")
    except mysql.connector.Error as err:
        print(f"Error al recuperar contraseña: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
