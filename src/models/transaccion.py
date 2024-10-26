class Transaccion:
    def __init__(self, id, cuit, codigo_accion, tipo, cantidad, precio, total, fecha):
        self.id = id
        self.cuit = cuit
        self.codigo_accion = codigo_accion
        self.tipo = tipo
        self.cantidad = cantidad
        self.precio = precio
        self.total = total
        self.fecha = fecha
