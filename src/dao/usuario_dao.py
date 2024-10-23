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