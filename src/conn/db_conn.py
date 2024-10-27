import mysql.connector


# Configuración de conexión
def connect_to_mysql():
    config = {
        "user": "uwjv6tgwnzz3xsj9",  # Reemplaza con tu usuario de Clever Cloud
        "password": "Rmrb4xAq9z6MrHFqai6L",  # Reemplaza con tu contraseña de Clever Cloud
        "host": "b9vkygdkqfhay1hkwomd-mysql.services.clever-cloud.com",  # Host correcto
        "database": "b9vkygdkqfhay1hkwomd",  # Nombre de la base de datos
        "raise_on_warnings": True,
    }

    try:
        # Estableciendo la conexión
        connection = mysql.connector.connect(**config)
        print("Conexión exitosa")
        return connection  # Devuelve la conexión

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None  # Devuelve None en caso de error


# El bloque de código anterior ahora está dentro de la función connect_to_mysql.
