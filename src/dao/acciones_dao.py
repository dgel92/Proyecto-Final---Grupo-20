from src.dao.interface_dao import DataAccessDAO
from src.model.acciones import Acciones
import mysql.connector
from mysql.connector import errorcode
from src.conn.db_conn import DBConn


class AccionesDAO(DataAccessDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn.connect_to_mysql()
        self.db_name = db_conn.get_data_base_name()


    def get(self, id: int) -> Acciones:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"SELECT id, nombre, valor_de_accion, cantidad_de_acciones FROM {self.db_name}.acciones WHERE id=%s"
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if row:
                    return Acciones(row[0], row[1], row[2], row[3])
                return None
            except mysql.connector.Error as err:
                raise err


    def get_all(self) -> list:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query=f"SELECT id, nombre, valor_de_accion, cantidad_de_acciones FROM {self.db_name}acciones"
                cursor.execute(query, )
                rows = cursor.fetchall()
                return [Acciones(row[0], row[1], row[2], row[3]) for row in rows] 
            except mysql.connector.Error as err:
                print(err)


    def create(self, accion: AccionesDAO):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"INSERT INTO {self.db_name}.acciones (id, name, valor_accion, cantidad_de_acciones) VALUES (%s, %s)"
                cursor.execute(query, (accion.id, accion.name, accion.valor_accion, accion.cantidad_de_acciones))
                conn.commit()
            except mysql.connector.Error as err:
                raise err


    def update(self, accion: AccionesDAO):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.db_name}.acciones SET id=%s, name=%s, valor_accion=%s, cantidad_de_acciones=%s"
                cursor.execute(query, (accion.id, accion.name, accion.valor_accion, accion.cantidad_de_acciones))
                conn.commit()
            except mysql.connector.Error as err:
                raise err


    def delete(self, accion_id: int):
        with self.db_conn as conn:
            try
                cursor = conn.cursor()
                query=f"DELETE FROM {self.db_name}.acciones WHERE id=%s"
                cursor.execute(query, (accion_id,))
                conn.comit()
            except mysql.connector.Error as err:
                raise err
