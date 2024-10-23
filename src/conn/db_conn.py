import mysql.connector
from mysql.connector import errorcode


class DBConn:
    def __init__(self, user, password, host, database, port):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database,
                port=self.port,
            )
            print("Conexión exitosa a la base de datos")
            return self.connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Usuario o contraseña incorrecta")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("La base de datos no existe")
            else:
                raise Exception(f"Error: {err}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    db_connection = DBConn(
        user="root",
        password="12345678",
        host="34.176.226.47",
        database="Base-proyecto",
        port="3306",
    )

    # Conectar a la base de datos
    connection = db_connection.connect()

    # Realiza tus operaciones aquí...

    # Cerrar la conexión
    db_connection.close()
