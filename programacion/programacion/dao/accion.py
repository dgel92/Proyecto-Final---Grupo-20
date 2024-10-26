import time

class Accion:
    def __init__(self, simbolo, precio_actual):
        self.simbolo = simbolo
        self.precio_actual = precio_actual

class Broker:
    def __init__(self, comision_porcentaje):
        self.comision_porcentaje = comision_porcentaje

    def calcular_comision(self, monto):
        return monto * self.comision_porcentaje / 100

class Venta:
    def __init__(self, accion, cantidad, broker):
        self.accion = accion
        self.cantidad = cantidad
        self.broker = broker

    def calcular_monto_venta(self):
        return self.accion.precio_actual * self.cantidad

    def calcular_comision_venta(self):
        return self.broker.calcular_comision(self.calcular_monto_venta())

    def es_venta_valida(self):
        return self.cantidad > 0 and self.accion.precio_actual > 0

def mostrar_precio_actual(accion):
    print(f"\n[*] Precio actual de {accion.simbolo}: ${accion.precio_actual:.2f}")

def realizar_venta(venta):
    if venta.es_venta_valida():
        print("\n[*] Procesando la venta...")
        time.sleep(1)  # Simula un pequeño retraso
        monto_venta = venta.calcular_monto_venta()
        comision_venta = venta.calcular_comision_venta()
        monto_neto = monto_venta - comision_venta
        
        print(f"[+] Venta realizada: {venta.cantidad} acciones de {venta.accion.simbolo} por ${monto_venta:.2f}")
        print(f"[+] Comisión del broker: ${comision_venta:.2f}")
        print(f"[+] Monto neto: ${monto_neto:.2f}\n")
    else:
        print("[!] Venta inválida")

# Ejemplo de uso
accion = Accion("DF", 100)
broker = Broker(2)
venta = Venta(accion, 10, broker)

mostrar_precio_actual(accion)
realizar_venta(venta)
