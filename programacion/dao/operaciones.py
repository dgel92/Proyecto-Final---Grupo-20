from registro import (
    Usuario,
    iniciar_sesion,
    recuperar_contrasena,
    mostrar_usuarios_registrados,
)
import json
import os


# Clase para manejar el portafolio de empresas y persistencia en JSON
class PortafolioEmpresas:
    def __init__(self, archivo_empresas="empresas.json"):
        self.archivo_empresas = archivo_empresas
        self.empresas = {}
        self.cargar_empresas()

    def cargar_empresas(self):
        """Cargar las empresas desde un archivo JSON si existe."""
        if os.path.exists(self.archivo_empresas):
            with open(self.archivo_empresas, "r") as archivo:
                empresas_data = json.load(archivo)
                for nombre, datos in empresas_data.items():
                    self.empresas[nombre] = {
                        "valor_por_accion": datos["valor_por_accion"],
                        "cantidad_acciones": datos["cantidad_acciones"],
                    }
        else:
            print(
                f"No se encontró el archivo {self.archivo_empresas}, se creará un nuevo archivo."
            )

    def guardar_empresas(self):
        """Guardar las empresas en un archivo JSON."""
        with open(self.archivo_empresas, "w") as archivo:
            json.dump(self.empresas, archivo, indent=4)
        print(f"Empresas guardadas en {self.archivo_empresas}.")

    def agregar_empresa(self, nombre, valor_por_accion, cantidad_acciones):
        """Agregar una nueva empresa al portafolio."""
        if nombre in self.empresas:
            print(f"Error: La empresa {nombre} ya existe.")
        else:
            self.empresas[nombre] = {
                "valor_por_accion": valor_por_accion,
                "cantidad_acciones": cantidad_acciones,
            }
            self.guardar_empresas()
            print(f"Empresa {nombre} agregada con éxito.")

    def eliminar_empresa(self, nombre):
        """Eliminar una empresa del portafolio."""
        if nombre in self.empresas:
            del self.empresas[nombre]
            self.guardar_empresas()
            print(f"Empresa {nombre} eliminada con éxito.")
        else:
            print(f"Error: La empresa {nombre} no existe.")

    def mostrar_empresas(self):
        """Mostrar todas las empresas del portafolio."""
        if not self.empresas:
            print("No hay empresas registradas.")
        else:
            for nombre, datos in self.empresas.items():
                print(f"Empresa: {nombre}")
                print(f"Valor por acción: ${datos['valor_por_accion']}")
                print(f"Cantidad de acciones disponibles: {datos['cantidad_acciones']}")

    def actualizar_valor_accion(self, nombre, nuevo_valor):
        """Actualizar el valor por acción de una empresa."""
        if nombre in self.empresas:
            self.empresas[nombre]["valor_por_accion"] = nuevo_valor
            self.guardar_empresas()
            print(f"Valor por acción de {nombre} actualizado a ${nuevo_valor}.")
        else:
            print(f"La empresa {nombre} no está registrada.")

    def modificar_cantidad_acciones(self, nombre, nueva_cantidad):
        """Modificar la cantidad de acciones disponibles de una empresa."""
        if nombre in self.empresas:
            self.empresas[nombre]["cantidad_acciones"] = nueva_cantidad
            self.guardar_empresas()
            print(f"Cantidad de acciones de {nombre} modificada a {nueva_cantidad}.")
        else:
            print(f"La empresa {nombre} no está registrada.")


class Operaciones:
    def __init__(self):
        self.portafolio = {}  # Diccionario para almacenar acciones y sus cantidades
        self.saldo = 1000000  # Inicializa el saldo, puede ser dinámico si deseas

    def compra(self, nombre_accion, cantidad, valor_por_accion):
        total_costo = cantidad * valor_por_accion
        if total_costo > self.saldo:
            print("Error: No tienes suficiente saldo para realizar esta compra.")
            return

        if nombre_accion in self.portafolio:
            self.portafolio[nombre_accion]["cantidad"] += cantidad
            self.portafolio[nombre_accion]["total_invertido"] += total_costo
        else:
            self.portafolio[nombre_accion] = {
                "cantidad": cantidad,
                "total_invertido": total_costo,
            }

        self.saldo -= total_costo  # Actualiza el saldo
        print(
            f"Compraste {cantidad} acciones de {nombre_accion} por ${valor_por_accion} cada una."
        )
        print(f"Saldo restante: ${self.saldo:.2f}")

    def venta(self, nombre_accion, cantidad):
        if (
            nombre_accion in self.portafolio
            and self.portafolio[nombre_accion]["cantidad"] >= cantidad
        ):
            valor_por_accion = (
                self.portafolio[nombre_accion]["total_invertido"]
                / self.portafolio[nombre_accion]["cantidad"]
            )
            total_ingreso = cantidad * valor_por_accion

            self.portafolio[nombre_accion]["cantidad"] -= cantidad
            self.saldo += total_ingreso  # Actualiza el saldo
            if self.portafolio[nombre_accion]["cantidad"] == 0:
                del self.portafolio[
                    nombre_accion
                ]  # Eliminar la acción si no quedan más

            print(f"Vendiste {cantidad} acciones de {nombre_accion}.")
            print(f"Saldo actualizado: ${self.saldo:.2f}")
        else:
            print("No tienes suficientes acciones para vender.")

    def ver_total_acciones(self):
        total_acciones = sum(info["cantidad"] for info in self.portafolio.values())
        return total_acciones

    def ver_saldo(self):
        return self.saldo


def mostrar_menu():
    print("\nMenú de Usuario:")
    print("1. Registrar nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Recuperar contraseña")
    print("4. Mostrar usuarios registrados")
    print("5. Salir")


def mostrar_menu_operaciones(operaciones, portafolio_empresas):
    while True:
        print("\nMenú de Operaciones:")
        print("1. Mostrar empresas disponibles")
        print("2. Comprar acciones")
        print("3. Vender acciones")
        print("4. Ver total de acciones compradas")
        print("5. Ver saldo")
        print("6. Salir al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            portafolio_empresas.mostrar_empresas()  # Mostrar empresas disponibles

        elif opcion == "2":
            nombre_accion = input("Nombre de la acción a comprar: ")
            cantidad = int(input("Cantidad de acciones a comprar: "))
            # Obtener valor por acción de la empresa
            if nombre_accion in portafolio_empresas.empresas:
                valor_por_accion = portafolio_empresas.empresas[
                    nombre_accion
                ].valor_por_accion
                operaciones.compra(nombre_accion, cantidad, valor_por_accion)
            else:
                print(f"La empresa {nombre_accion} no está registrada.")

        elif opcion == "3":
            nombre_accion = input("Nombre de la acción a vender: ")
            cantidad = int(input("Cantidad de acciones a vender: "))
            operaciones.venta(nombre_accion, cantidad)

        elif opcion == "4":
            total = operaciones.ver_total_acciones()
            print(f"Total de acciones compradas: {total}")

        elif opcion == "5":
            saldo = operaciones.ver_saldo()
            print(f"Saldo actual: ${saldo:.2f}")

        elif opcion == "6":
            print("Saliendo al menú principal.")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")


def ejecutar_menu():
    portafolio_empresas = PortafolioEmpresas()  # Inicializar el portafolio de empresas
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
            if iniciar_sesion(
                email, password
            ):  # Verifica si el inicio de sesión fue exitoso
                operaciones = Operaciones()  # Inicializar la clase Operaciones
                mostrar_menu_operaciones(
                    operaciones, portafolio_empresas
                )  # Mostrar el menú de operaciones

        elif opcion == "3":
            email = input("Email: ")
            nueva_password = input("Nueva contraseña: ")
            respuesta_seguridad = input("Respuesta a la pregunta de seguridad: ")
            recuperar_contrasena(email, nueva_password, respuesta_seguridad)

        elif opcion == "4":
            mostrar_usuarios_registrados()

        elif opcion == "5":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


# Ejemplo de uso
if __name__ == "__main__":
    ejecutar_menu()
