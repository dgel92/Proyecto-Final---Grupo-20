import json
import os
from datetime import datetime
from registro import cargar_usuarios, guardar_usuarios

archivo_usuarios = "usuarios.json"

usuarios = cargar_usuarios()


class PanelDeControl:
    def __init__(self, email):
        if email not in usuarios:
            print(f"Error: El usuario con email {email} no está registrado.")
            return
        self.usuario = usuarios[email]

    def agregar_transaccion(self, tipo, monto):
        """Agregar una transacción al historial."""
        transaccion = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": tipo, 
            "monto": monto,
        }
        self.usuario["transacciones"].append(transaccion)
        self.usuario["saldo"] += monto if tipo == "depósito" else -monto
        guardar_usuarios()

    def mostrar_panel_control(self):
        """Mostrar el saldo, historial de transacciones y rendimiento de inversiones."""
        print(
            f"Panel de control de {self.usuario['nombre']} {self.usuario['apellido']}:"
        )
        print(f"Saldo actual: ${self.usuario['saldo']}")
        print("Historial de transacciones:")
        for transaccion in self.usuario["transacciones"]:
            print(
                f"- {transaccion['fecha']}: {transaccion['tipo']} de ${transaccion['monto']}"
            )

        print("Rendimiento de inversiones:")
        if self.usuario["inversiones"]:
            for inversion in self.usuario["inversiones"]:
                print(
                    f"- Inversión en {inversion['nombre']} con rendimiento del {inversion['rendimiento']}%"
                )
        else:
            print("No hay inversiones registradas.")

    def agregar_inversion(self, nombre_inversion, monto, rendimiento):
        """Agregar una inversión al historial."""
        inversion = {
            "nombre": nombre_inversion,
            "monto": monto,
            "rendimiento": rendimiento,  # En porcentaje
        }
        self.usuario["inversiones"].append(inversion)
        guardar_usuarios()
