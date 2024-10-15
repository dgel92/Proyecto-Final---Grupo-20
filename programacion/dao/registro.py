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
    usuario["password"] = hashed_password.decode("utf-8")
    usuario["bloqueado"] = False
    usuario["intentos_fallidos"] = 0

    guardar_usuarios()
    print("Contraseña actualizada exitosamente y cuenta desbloqueada.")


# Prueba creando un objeto Usuario y registrando
nuevo_usuario = Usuario(
    "Juan",
    "Pérez",
    "20-12345678-9",
    "juan.perez@gmail.com",
    "password123",
    "¿Cuál es el nombre de tu primera mascota?",
    "Firulais",
)
nuevo_usuario.guardar()

mostrar_usuarios_registrados()

email_usuario = "juan.perez@gmail.com"
iniciar_sesion(email_usuario, "password123")
iniciar_sesion(email_usuario, "incorrecto1")
iniciar_sesion(email_usuario, "incorrecto2")
iniciar_sesion(email_usuario, "incorrecto3")

nueva_contrasena = "nueva_password123"
respuesta_usuario = "Firulais"
recuperar_contrasena(email_usuario, nueva_contrasena, respuesta_usuario)

mostrar_usuarios_registrados()
