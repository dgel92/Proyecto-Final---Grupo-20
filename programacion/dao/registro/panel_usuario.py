from programacion.dao.registro.registro_usuario import (
    Usuario,
    iniciar_sesion,
    recuperar_contrasena,
    mostrar_usuarios_registrados,
)


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
