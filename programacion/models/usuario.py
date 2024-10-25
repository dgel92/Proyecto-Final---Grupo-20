class Usuario:
    def __init__(self, cuil, nombre, apellido, email, password, saldo, intentos_fallidos, bloqueado):
        self.cuil = cuil
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
        self.saldo = saldo
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado = bloqueado
