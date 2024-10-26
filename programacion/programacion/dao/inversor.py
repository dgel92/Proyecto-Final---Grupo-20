class Inversor:
    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self.saldo = saldo

    def actualizar_saldo(self, monto):
        self.saldo += monto

class Operacion:
    def __init__(self, tipo, monto, comision):
        self.tipo = tipo
        self.monto = monto
        self.comision = comision

    def calcular_monto_neto(self):
        return self.monto - (self.monto * self.comision / 100)

def registrar_operacion(inversor, operacion):
    monto_neto = operacion.calcular_monto_neto()
    inversor.actualizar_saldo(monto_neto)
    print(f"[*] Operación registrada: {operacion.tipo} por ${operacion.monto:.2f} (comisión {operacion.comision}%)")
    print(f"[+] Saldo actual de {inversor.nombre}: ${inversor.saldo:.2f}")

# Ejemplo de uso
inversor = Inversor("Juan", 1000)
operacion = Operacion("Venta", 500, 5)

registrar_operacion(inversor, operacion)
