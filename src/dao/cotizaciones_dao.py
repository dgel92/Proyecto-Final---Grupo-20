from src.dao.interface_dao import DataAccessDAO
from src.model.acciones import Acciones
import mysql.connector
from mysql.connector import errorcode
from src.conn.db_conn import DBConn


class CotizacionesDAO(DataAccessDAO):
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn.connect_to_mysql()
        self.db_name = db_conn.get_data_base_name()


    def get(self, id: int) -> Cotizaciones:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"SELECT id, accion_id, fecha, valor_accion FROM {self.db_name}.cotizaciones WHERE id=%s"
                cursor.execute(query, (id,))
                row = cursor.fetchone()
                if row:
                    return Cotizaciones(row[0], row[1], row[2], row[3])
                return None
            except mysql.connector.Error as err:
                raise err


    def get_all(self) -> list:
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query=f"SELECT id, accion_id, fecha, valor_accion FROM {self.db_name}.cotizaciones"
                cursor.execute(query, )
                rows = cursor.fetchall()
                return [Cotizaciones(row[0], row[1], row[2], row[3]) for row in rows] 
            except mysql.connector.Error as err:
                print(err)


    def create(self, cotizaciones: CotizacionesDAO):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"INSERT INTO {self.db_name}.cotizaciones (id, accion_id, fecha, valor_accion) VALUES (%s, %s)"
                cursor.execute(query, (cotizaciones.id, cotizaciones.accion_id, cotizaciones.fecha, cotizaciones.valor_accion))
                conn.commit()
            except mysql.connector.Error as err:
                raise err


    def update(self, cotizaciones: CotizacionesDAO):
        with self.db_conn as conn:
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.db_name}.cotizaciones SET id=%s, accion_id=%s, fecha=%s, valor_accion=%s"
                cursor.execute(query, (cotizaciones.id, cotizaciones.accion_id, cotizaciones.fecha, cotizaciones.valor_accion))
                conn.commit()
            except mysql.connector.Error as err:
                raise err


    def delete(self, cotizacion_id: int):
        with self.db_conn as conn:
            try
                cursor = conn.cursor()
                query=f"DELETE FROM {self.db_name}.cotizaciones WHERE id=%s"
                cursor.execute(query, (cotizacion_id,))
                conn.comit()
            except mysql.connector.Error as err:
                raise err
