import bcrypt
import json
import os

archivo_usuarios = "usuarios.json"


def cargar_usuarios():
    if os.path.exists(archivo_usuarios):
        with open(archivo_usuarios, "r") as archivo:
            return json.load(archivo)
    return {}


def guardar_usuarios():
    with open(archivo_usuarios, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)


usuarios = cargar_usuarios()


def registrar_usuario(
    nombre, apellido, cuil, email, password, pregunta_seguridad, respuesta_seguridad
):
    if any(user["cuil"] == cuil for user in usuarios.values()) or email in usuarios:
        print("Error: El CUIL o el email ingresados ya están registrados.")
        return

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    saldo_inicial = 1000000.0

    usuarios[email] = {
        "nombre": nombre,
        "apellido": apellido,
        "cuil": cuil,
        "password": hashed_password.decode("utf-8"),
        "intentos_fallidos": 0,
        "bloqueado": False,
        "saldo": saldo_inicial,
        "pregunta_seguridad": pregunta_seguridad,
        "respuesta_seguridad": respuesta_seguridad,
    }

    guardar_usuarios()
    print(f"Usuario registrado exitosamente con un saldo inicial de ${saldo_inicial}.")


def mostrar_usuarios_registrados():
    if not usuarios:
        print("No hay usuarios registrados.")
    else:
        for email, datos in usuarios.items():
            print(f"Email: {email}")
            print(f"Nombre: {datos['nombre']} {datos['apellido']}")
            print(f"CUIL: {datos['cuil']}")
            print(f"Saldo: ${datos['saldo']}")
            print(f"Bloqueado: {datos['bloqueado']}")
            print("-" * 20)


def iniciar_sesion(email, password):
    if email not in usuarios:
        print("Error: El email ingresado no está registrado.")
        return

    usuario = usuarios[email]

    if usuario["bloqueado"]:
        print(
            "Su cuenta está bloqueada. Debe cambiar la contraseña para poder iniciar sesión."
        )
        return

    if bcrypt.checkpw(password.encode("utf-8"), usuario["password"].encode("utf-8")):
        print(f"Bienvenido {usuario['nombre']}!")
        usuario["intentos_fallidos"] = 0
    else:
        usuario["intentos_fallidos"] += 1
        print("Contraseña incorrecta.")
        if usuario["intentos_fallidos"] >= 3:
            usuario["bloqueado"] = True
            print(
                "Ha superado el número de intentos fallidos. Su cuenta ha sido bloqueada."
            )

    guardar_usuarios()


def recuperar_contrasena(email, nueva_password, respuesta_seguridad):
    if email not in usuarios:
        print("Error: El email ingresado no está registrado.")
        return

    usuario = usuarios[email]

    if usuario["respuesta_seguridad"] != respuesta_seguridad:
        print("Error: Respuesta de seguridad incorrecta.")
        return

    hashed_password = bcrypt.hashpw(nueva_password.encode("utf-8"), bcrypt.gensalt())
    usuario["password"] = hashed_password.decode(
        "utf-8"
    )  # Actualizar el hash de la contraseña

    usuario["bloqueado"] = False
    usuario["intentos_fallidos"] = 0

    guardar_usuarios()
    print("Contraseña actualizada exitosamente y cuenta desbloqueada.")


# Prueba
registrar_usuario(
    "Juan",
    "Pérez",
    "20-12345678-9",
    "juan.perez@gmail.com",
    "password123",
    "¿Cuál es el nombre de tu primera mascota?",
    "Firulais",
)

# Mostrar usuarios registrados
mostrar_usuarios_registrados()

# Prueba de logueo
email_usuario = "juan.perez@gmail.com"
iniciar_sesion(email_usuario, "password123")
iniciar_sesion(email_usuario, "incorrecto1")
iniciar_sesion(email_usuario, "incorrecto2")
iniciar_sesion(email_usuario, "incorrecto3")

# Prueba TDD de ver si se guardaron los cambios en el JSON
mostrar_usuarios_registrados()

# Prueba TDD de recupero de contraseña
nueva_contrasena = "nueva_password123"
respuesta_usuario = "Firulais"
recuperar_contrasena(email_usuario, nueva_contrasena, respuesta_usuario)

# Prueba TDD
mostrar_usuarios_registrados()
