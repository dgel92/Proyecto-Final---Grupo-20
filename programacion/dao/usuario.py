import bcrypt
import json
import os

# Archivo provisorio para generar persistencia
archivo_usuarios = "usuarios.json"


# Cargar los usuarios desde el JSON al iniciar el programa
def cargar_usuarios():
    if os.path.exists(archivo_usuarios):
        with open(archivo_usuarios, "r") as archivo:
            return json.load(archivo)
    return {}


def guardar_usuarios():
    with open(archivo_usuarios, "w") as archivo:
        json.dump(usuarios, archivo, indent=4)


usuarios = cargar_usuarios()


def registrar_usuario(nombre, apellido, cuil, email, password):
    if any(user["cuil"] == cuil for user in usuarios.values()) or email in usuarios:
        print("Error: El CUIL o el email ingresados ya están registrados.")
        return

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    saldo_inicial = 1000000.0

    usuarios[email] = {
        "nombre": nombre,
        "apellido": apellido,
        "cuil": cuil,
        "password": hashed_password.decode(
            "utf-8"
        ),  # Convertimos el hash a string para JSON
        "intentos_fallidos": 0,
        "bloqueado": False,
        "saldo": saldo_inicial,
    }

    guardar_usuarios()  # Guardar los usuarios actualizados en el archivo JSON
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
            print("-" * 20)


# Ejemplo de uso
registrar_usuario(
    "Juan", "Pérez", "20-12345678-9", "juan.perez@gmail.com", "password123"
)

# Mostrar usuarios registrados
mostrar_usuarios_registrados()
