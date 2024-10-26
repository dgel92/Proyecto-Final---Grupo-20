<<<<<<< HEAD
from src.dao.interface_dao import DataAccessDAO
from src.model.acciones import Acciones
import mysql.connector
from mysql.connector import errorcode
from src.conn.db_conn import DBConn


class UsuarioDAO(DataAccessDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn.connect_to_mysql()
        self.db_name = db_conn.get_data_base_name()


        def get(self, id: int) -> Usuario:
            with self.db_conn as conn:
                try:
                    cursor = conn.cursor()
                    query = f"SELECT id, nombre, apelllido, cuil, email FROM {self.db_name}.usuario where id=%s"
                    cursor.execute(query, (id,))
                    row = cursor.fetchone()
                    if row:
                        return Usuario(row[0], row[1], row[2], row[3])
                    return None
                except mysql.connector.Error as err:
                    raise err


    def get_all(self) -> list:
        with self.db_conn as conn:
                try:
                    cursor = conn.cursor()
                    query = f"SELECT id, nombre, apelllido, cuil, email FROM {self.db_name}.usuario where id=%s"
                    cursor.execute(query, )
                    row = cursor.fetchone()
                    return [Usuario(row[0], row[1], row[2], row[3]) for row in rows]
                except mysql.connector.Error as err:
                    print(err)


    def create(self, usuario: UsuarioDAO)
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"INSERT INTO {self.db_name}.usuario (id, nombre, apellido, cuil, email, password, pregunta_seguridad, respuesta_seguridad, intentos_fallidos, bloquedao, saldo) VALUES(%s, %s, %s)"
                cursor.execute(query, (usuario.id, usuario.name, usuario.apelllido, usuario.cuil, usuario.email, usuario.password, usuario.pregunta_seguridad, usuario.respuesta_seguridad, usuario.intentos_fallidos, usuario.bloqueado, usuario.saldo))
                conn.commit()
            except mysql.connector.Error as err:
                raise err
            
def update(self, usuario: UsuarioDAO):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.db_name}.usuario SET id=%s, nombre=%s, apellido=%s, cuil=%s, email=%s, password=%s, pregunta_seguridad=%s, respuesta_seguridad=%s, intentos_faliidos=%s, bloqueado=%s, saldo=%s"
                cursor.execute(query, (usuario.id, usuario.nombre, usuario.apellido, usuario.cuil, usuario.email, usuario.password, usuario.pregunta_seguridad, usuario.respuesta_seguridad, usuario.intentos_fallidos, usuario.bloqueado, usuario.saldo))
                conn.commit()
            except mysql.connector.Error as err:
                raise err
            
def delete(self, usuario_id: int):
        with self.db_conn as conn:
            try
                cursor = conn.cursor()
                query=f"DELETE FROM {self.db_name}.usuario WHERE id=%s"
                cursor.execute(query, (usuario_id,))
                conn.comit()
            except mysql.connector.Error as err:
                raise err
=======
import sys
import os
import mysql.connector
from mysql.connector import errorcode
import bcrypt
from decimal import Decimal

# Añadir el directorio base del proyecto al sys.path para resolver las importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conn.conn_db import conectar_bd

class UsuarioDAO:
    def __init__(self):
        self.conn = conectar_bd()

    def registrar_usuario(self, cuit, nombre, apellido, email, password):
        cursor = self.conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        saldo_inicial = Decimal('1000000.00')
        try:
            cursor.execute("""
                INSERT INTO inversores (cuit, nombre, apellido, email, contraseña, saldo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cuit, nombre, apellido, email, hashed_password.decode('utf-8'), saldo_inicial))
            self.conn.commit()
        except mysql.connector.Error as err:
            print("Error al registrar el usuario: {}".format(err))
        finally:
            cursor.close()

    def iniciar_sesion(self, email, password):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inversores WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario and bcrypt.checkpw(password.encode('utf-8'), usuario['contraseña'].encode('utf-8')):
            print("Inicio de sesión exitoso.")
            return usuario
        else:
            print("Correo electrónico o contraseña incorrectos.")
            return None

    def recuperar_contraseña(self, email):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT contraseña FROM inversores WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        cursor.close()

        if usuario:
            print(f"Tu contraseña es: {usuario['contraseña']}")
        else:
            print("Correo electrónico no registrado.")

    def cerrar_conexion(self):
        self.conn.close()

# Pruebas de ejemplo
if __name__ == "__main__":
    usuario_dao = UsuarioDAO()

    # Registrar un usuario de prueba
    usuario_dao.registrar_usuario('20304050607', 'Juan', 'Pérez', 'juan.perez@gmail.com', '123456')

    # Iniciar sesión con un usuario de prueba
    usuario = usuario_dao.iniciar_sesion('juan.perez@gmail.com', '123456')
    if usuario:
        print(usuario)
    
    # Recuperar contraseña del usuario
    usuario_dao.recuperar_contraseña('juan.perez@gmail.com')

    # Cerrar la conexión a la base de datos
    usuario_dao.cerrar_conexion()
>>>>>>> nahir
