class Usuario:
    def __init__(
        self,
        id: int,
        nombre: str,
        apellido: str,
        cuil: int,
        email: str,
        password: str,
        pregunta_seguridad: str,
        respuesta_seguridad: str,
        intentos_fallidos: int,
        bloqueado: bool,
        saldo: int,
    ):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.cuil = cuil
        self.email = email
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.pregunta_seguridad = pregunta_seguridad
        self.respuesta_seguridad = respuesta_seguridad
        self.intentos_fallidos = intentos_fallidos
        self.bloqueado = bloqueado
        self.saldo = saldo
