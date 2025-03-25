"""importa libreria."""

import json


class Calculadora:  # ← D101: Missing docstring in public class
    """Calcula operaciones matematicas."""

    def __init__(self):
        """Manda a llamar el historia."""
        self.historial = []

    def sumar(self, a, b):  # ← D103: Missing docstring in public function
        """Realiza sumas."""
        resultado = a + b
        self.historial.append({"operacion": "suma", "resultado": resultado})
        return resultado

    def restar(self, a, b):
        """Realiza restas."""
        resultado = a - b
        self.historial.append({"operacion": "resta", "resultado": resultado})
        return resultado  # ← falta espacio tras coma, mal formato

    def imprimir_historial(self):
        """Imprime operacion y resultado."""
        for entrada in self.historial:
            print(
                entrada["operacion"], ":", entrada["resultado"]
            )  # ← black cambiaría el estilo, falta espaciado

    def guardar_historial(self, archivo):
        """Guarda historial."""
        print("Guardando...")
        with open(archivo, "w") as f:
            json.dump(self.historial, f, indent=4)


def ejecutar():
    """Guarda historial."""
    print("Iniciando ejecución")  # ← sin docstring, estilo incorrecto


calc = Calculadora()
calc.sumar(5, 3)
calc.restar(10, 2)
calc.imprimir_historial()
calc.guardar_historial("historial.json")
