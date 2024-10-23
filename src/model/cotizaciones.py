class Cotizaciones:
    def __init__(self, id: int, accion_id: int, fecha: date, valor_accion: decimal):
        self.id = id
        self.accion_id = accion_id
        self.fecha = fecha
        self.valor_accion = valor_accion

    def __repr__(self):
        return f"Cotizacion(id={self.id}, Accion={self.accion_id}, Fecha_cotizacion={self.fecha}, valor_de_la_accion={self.valor_accion})"
