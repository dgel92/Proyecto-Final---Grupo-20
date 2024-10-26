import time

class Accion:
    def __init__(self, simbolo, precio):
        self.simbolo = simbolo
        self.precio = precio

def actualizar_portfolio(portfolio, accion, cantidad):
    if accion.simbolo in portfolio:
        print(f"[*] Vendiendo {cantidad} acciones de {accion.simbolo}...")
        time.sleep(1)  # Simulando un proceso
        portfolio[accion.simbolo] -= cantidad
        
        if portfolio[accion.simbolo] <= 0:
            del portfolio[accion.simbolo]
            print(f"[!] {accion.simbolo} eliminado del portfolio.")
        else:
            print(f"[+] {cantidad} acciones de {accion.simbolo} vendidas. {portfolio[accion.simbolo]} restantes.")
    else:
        print("[!] La acción no está en el portfolio.")

# Inicializando la acción y el portfolio
accion = Accion("DF", 100)
portfolio = {"DF": 20, "OTRA": 10}

print("[*] Portfolio antes de la venta:")
print(portfolio)

cantidad_vendida = 10
actualizar_portfolio(portfolio, accion, cantidad_vendida)

print("[*] Portfolio después de la venta:")
print(portfolio)
