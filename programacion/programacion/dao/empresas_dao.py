import json
import os


class Empresa:
    def __init__(self, nombre, valor_por_accion, cantidad_acciones):
        self.nombre = nombre
        self.valor_por_accion = valor_por_accion
        self.cantidad_acciones = cantidad_acciones

    def mostrar_info(self):
        """Mostrar la información de la empresa."""
        print(f"Empresa: {self.nombre}")
        print(f"Valor por acción: ${self.valor_por_accion}")
        print(f"Cantidad de acciones disponibles: {self.cantidad_acciones}")

    def actualizar_valor_accion(self, nuevo_valor):
        """Actualizar el valor por acción."""
        self.valor_por_accion = nuevo_valor

    def modificar_cantidad_acciones(self, nueva_cantidad):
        """Modificar la cantidad de acciones disponibles."""
        self.cantidad_acciones = nueva_cantidad


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
                    self.empresas[nombre] = Empresa(
                        nombre,
                        datos["valor_por_accion"],
                        datos["cantidad_acciones"],
                    )
        else:
            print(
                f"No se encontró el archivo {self.archivo_empresas}, se creará un nuevo archivo."
            )

    def guardar_empresas(self):
        """Guardar las empresas en un archivo JSON."""
        empresas_data = {
            nombre: {
                "valor_por_accion": empresa.valor_por_accion,
                "cantidad_acciones": empresa.cantidad_acciones,
            }
            for nombre, empresa in self.empresas.items()
        }
        with open(self.archivo_empresas, "w") as archivo:
            json.dump(empresas_data, archivo, indent=4)
        print(f"Empresas guardadas en {self.archivo_empresas}.")

    def agregar_empresa(self, nombre, valor_por_accion, cantidad_acciones):
        """Agregar una nueva empresa al portafolio."""
        if nombre in self.empresas:
            print(f"Error: La empresa {nombre} ya existe.")
        else:
            nueva_empresa = Empresa(nombre, valor_por_accion, cantidad_acciones)
            self.empresas[nombre] = nueva_empresa
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
            for empresa in self.empresas.values():
                empresa.mostrar_info()


# Función para mostrar el menú interactivo
def menu():
    portafolio = PortafolioEmpresas()

    while True:
        print("\n--- Menú Principal ---")
        print("1. Mostrar todas las empresas")
        print("2. Agregar una nueva empresa")
        print("3. Eliminar una empresa")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Mostrar todas las empresas
            portafolio.mostrar_empresas()

        elif opcion == "2":
            # Agregar una nueva empresa
            nombre = input("Ingrese el nombre de la empresa: ")
            valor_por_accion = float(input("Ingrese el valor por acción: "))
            cantidad_acciones = int(input("Ingrese la cantidad de acciones: "))
            portafolio.agregar_empresa(nombre, valor_por_accion, cantidad_acciones)

        elif opcion == "3":
            # Eliminar una empresa
            nombre = input("Ingrese el nombre de la empresa a eliminar: ")
            portafolio.eliminar_empresa(nombre)

        elif opcion == "4":
            # Salir del programa
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")


# Ejemplo de uso
if __name__ == "__main__":
    menu()
