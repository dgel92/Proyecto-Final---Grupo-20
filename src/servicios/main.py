from ..conn.db_conn import connect_to_mysql
from ..dao.empresa_dao import (
    EmpresaDAO,
)  # Asegúrate de tener la importación correcta de tu DAO
from ..models.empresa import Empresa  # Importa tu clase Empresa correctamente


# Función para pedir los datos de la empresa por consola
def input_empresa_data():
    nombre = input("Ingrese el nombre de la empresa: ")
    valor_de_accion = int(input("Ingrese el valor de la acción: "))
    cantidad_de_acciones = int(input("Ingrese la cantidad de acciones: "))
    return Empresa(nombre, valor_de_accion, cantidad_de_acciones)


# Función principal
if __name__ == "__main__":
    # Conectar a la base de datos
    connection = connect_to_mysql()

    # Crear el DAO de empresas
    empresa_dao = EmpresaDAO(connection)

    # Pedir los datos de la empresa por consola
    nueva_empresa = input_empresa_data()

    # Guardar la nueva empresa en la base de datos
    empresa_dao.create(nueva_empresa)

    # Mostrar todas las empresas en la base de datos
    empresas = empresa_dao.get_all()
    print("Empresas en la base de datos:", empresas)

    # Cerrar la conexión
    connection.close()
