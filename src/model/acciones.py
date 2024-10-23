class Acciones:
    def __init__(
        self, id: int, nombre: str, valor_de_accion: int, cantidad_de_acciones: int
    ):
        self.id = id
        self.nombre = nombre
        self.valor_de_accion = valor_de_accion
        self.cantidad_de_acciones = cantidad_de_acciones

    def __repr__(self):
        return f"Empresa(id={self.id}, nombre={self.nombre}, valor_de_accion={self.valor_de_accion}, cantidad_de_acciones={self.cantidad_de_acciones})"
