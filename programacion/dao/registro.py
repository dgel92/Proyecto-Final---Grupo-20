import bcrypt
import json
import os

archivo_usuarios = "usuarios.json"


def cargar_usuarios():
    if os.path.exists(archivo_usuarios):
        with open(archivo_usuarios, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}


def guardar_usuarios():
    with open(archivo_usuarios, "w", encoding="utf-8") as file:
        json.dump(usuarios, file, indent=4, ensure_ascii=False)


usuarios = cargar_usuarios()


class Usuario:
    def __init__(
        self,
        nombre,
        apellido,
        cuil,
        email,
        password,
        pregunta_seguridad,
        respuesta_seguridad,
    ):
        self.nombre = nombre
        self.apellido = apellido
        self.cuil = cuil
        self.email = email
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.pregunta_seguridad = pregunta_seguridad
        self.respuesta_seguridad = respuesta_seguridad
        self.intentos_fallidos = 0
        self.bloqueado = False
        self.saldo = 1000000.0

    def guardar(self):
        if (
            any(user["cuil"] == self.cuil for user in usuarios.values())
            or self.email in usuarios
        ):
            print("Error: El CUIL o el email ingresados ya están registrados.")
            return

        usuarios[self.email] = {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "cuil": self.cuil,
            "password": self.hashed_password,
            "intentos_fallidos": self.intentos_fallidos,
            "bloqueado": self.bloqueado,
            "saldo": self.saldo,
            "pregunta_seguridad": self.pregunta_seguridad,
            "respuesta_seguridad": self.respuesta_seguridad,
        }

        guardar_usuarios()
        print(f"Usuario registrado exitosamente con un saldo inicial de ${self.saldo}.")


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
        return False  # Retorna False si el email no está registrado

    usuario = usuarios[email]

    if usuario["bloqueado"]:
        print(
            "Su cuenta está bloqueada. Debe cambiar la contraseña para poder iniciar sesión."
        )
        return False  # Retorna False si la cuenta está bloqueada

    if bcrypt.checkpw(password.encode("utf-8"), usuario["password"].encode("utf-8")):
        print(f"Bienvenido {usuario['nombre']}!")
        usuario["intentos_fallidos"] = 0
        return True  # Retorna True si el inicio de sesión es exitoso
    else:
        usuario["intentos_fallidos"] += 1
        print("Contraseña incorrecta.")
        if usuario["intentos_fallidos"] >= 3:
            usuario["bloqueado"] = True
            print(
                "Ha superado el número de intentos fallidos. Su cuenta ha sido bloqueada."
            )
        return False  # Retorna False si la contraseña es incorrecta

    guardar_usuarios()  # Asegúrate de que esto esté fuera de las condiciones


def recuperar_contrasena(email, nueva_password, respuesta_seguridad):
    if email not in usuarios:
        print("Error: El email ingresado no está registrado.")
        return

    usuario = usuarios[email]

    if usuario["respuesta_seguridad"] != respuesta_seguridad:
        print("Error: Respuesta de seguridad incorrecta.")
        return

    hashed_password = bcrypt.hashpw(nueva_password.encode("utf-8"), bcrypt.gensalt())
    usuario["password"] = hashed_password.decode("utf-8")
    usuario["bloqueado"] = False
    usuario["intentos_fallidos"] = 0

    guardar_usuarios()
    print("Contraseña actualizada exitosamente y cuenta desbloqueada.")
