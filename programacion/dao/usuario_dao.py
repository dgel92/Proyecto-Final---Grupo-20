from conn.conn_db import conectar_bd

class InversorDAO:
    def __init__(self):
        self.conn = conectar_bd()

    def mostrar_datos_cuenta(self, cuit):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inversores WHERE cuit = %s", (cuit,))
        usuario = cursor.fetchone()
        cursor.close()
        if usuario:
            print(f"Saldo actual: {usuario['saldo']}")
            print(f"Nombre: {usuario['nombre']}, Apellido: {usuario['apellido']}, CUIT: {usuario['cuit']}")
        else:
            print("Inversor no encontrado")

    def calcular_rendimiento_total(self, cuit):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT SUM((a.precio_venta - a.precio_compra) * t.cantidad) AS rendimiento_total
            FROM transacciones t
            JOIN acciones a ON t.codigo_accion = a.codigo
            WHERE t.cuit = %s AND t.tipo = 'compra'
        """, (cuit,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            print(f"Rendimiento total de la cuenta: {resultado['rendimiento_total']:.2f}")
        else:
            print("No se encontraron transacciones de compra para este inversor.")
    
    def listar_activos_portafolio(self, cuit):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.nombre, t.cantidad, a.precio_compra, a.precio_venta
            FROM transacciones t
            JOIN acciones a ON t.codigo_accion = a.codigo
            WHERE t.cuit = %s AND t.tipo = 'compra'
        """, (cuit,))
        activos = cursor.fetchall()
        cursor.close()
        for activo in activos:
            rendimiento = (activo['precio_venta'] - activo['precio_compra']) / activo['precio_compra'] * 100
            print(f"Nombre: {activo['nombre']}, Cantidad: {activo['cantidad']}, Precio Compra: {activo['precio_compra']}, Precio Venta: {activo['precio_venta']}, Rendimiento: {rendimiento:.2f}%")

    def cerrar_conexion(self):
        self.conn.close()

# Pruebas de ejemplo
if __name__ == "__main__":
    inversor_dao = InversorDAO()
    
    # Mostrar datos de la cuenta
    inversor_dao.mostrar_datos_cuenta('20304050607')
    
    # Calcular el rendimiento total de la cuenta
    inversor_dao.calcular_rendimiento_total('20304050607')
    
    # Listar activos del portafolio
    inversor_dao.listar_activos_portafolio('20304050607')
    
    # Cerrar la conexión a la base de datos
    inversor_dao.cerrar_conexion()
