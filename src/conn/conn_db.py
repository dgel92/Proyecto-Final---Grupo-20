import mysql.connector
from mysql.connector import errorcode

def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Ramona23',
            database='ARGBroker'
        )
        print("Conexión exitosa a la base de datos.")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error con el nombre de usuario o la contraseña.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        else:
            print(err)

# Ejemplo de uso
if __name__ == "__main__":
    conectar_bd()
