from src.servicios.registro.registro_usuario import (
    iniciar_sesion,
    recuperar_contrasena,
    mostrar_usuarios_registrados,
    registrar_usuario,
)


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
        # Se realiza el hash de la contraseña para almacenar de forma segura
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.pregunta_seguridad = pregunta_seguridad
        self.respuesta_seguridad = respuesta_seguridad
        self.intentos_fallidos = 0
        self.bloqueado = False
        self.saldo = 0.0

    def guardar(self):
        # Llama a la función registrar_usuario para almacenar el usuario en la base de datos
        registrar_usuario(self)


def mostrar_menu():
    print("\nMenú de Usuario:")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Recuperar contraseña")
    print("4. Mostrar usuarios registrados")
    print("5. Salir")


def ejecutar_menu():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            cuil = input("CUIL: ")
            email = input("Email: ")
            password = input("Contraseña: ")
            pregunta_seguridad = input("Pregunta de seguridad: ")
            respuesta_seguridad = input("Respuesta de seguridad: ")

            nuevo_usuario = Usuario(
                nombre,
                apellido,
                cuil,
                email,
                password,
                pregunta_seguridad,
                respuesta_seguridad,
            )
            nuevo_usuario.guardar()

        elif opcion == "2":
            email = input("Email: ")
            password = input("Contraseña: ")
            iniciar_sesion(email, password)

        elif opcion == "3":
            email = input("Email: ")
            nueva_password = input("Nueva contraseña: ")
            respuesta_seguridad = input("Respuesta a la pregunta de seguridad: ")
            recuperar_contrasena(email, nueva_password, respuesta_seguridad)

        elif opcion == "4":
            mostrar_usuarios_registrados()

        elif opcion == "5":
            print("Saliendo del programa.")
            break

        else:
            print("Opción no válida. Por favor, elige una opción del menú.")


# Ejecutar el menú
if __name__ == "__main__":
    ejecutar_menu()
