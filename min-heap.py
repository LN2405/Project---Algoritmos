from datetime import datetime

class MinHeapAlimentos:

    def __init__(self):
        self.heap = []

    def insertar_alimento(self, nombre, cantidad, lugar, fecha_vencimiento):

        fecha = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")

        alimento = {
            "nombre": nombre,
            "cantidad": cantidad,
            "lugar": lugar,
            "fecha": fecha
        }

        self.heap.append(alimento)

        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):

        while index > 0:

            parent = (index - 1) // 2

            if self.heap[index]["fecha"] < self.heap[parent]["fecha"]:

                self.heap[index], self.heap[parent] = \
                self.heap[parent], self.heap[index]

                index = parent

            else:
                break

    def ver_proximo_vencer(self):

        if not self.heap:
            return "No hay alimentos registrados"

        return self.heap[0]

    def mostrar(self):

        if not self.heap:
            print("No hay alimentos registrados")
            return

        for alimento in self.heap:

            print(
                alimento["nombre"],
                "- cantidad:", alimento["cantidad"],
                "- lugar:", alimento["lugar"],
                "- vence:",
                alimento["fecha"].strftime("%Y-%m-%d")
            )

sistema = MinHeapAlimentos()

sistema.insertar_alimento("Leche", 20, "Supermercado Plaza", "2026-05-25")

sistema.insertar_alimento("Pan", 15, "Restaurante Sol", "2026-05-20")

sistema.insertar_alimento("Queso", 10, "Market Food", "2026-05-22")

print("Alimento que vencerá primero:")
print(sistema.ver_proximo_vencer())

print("\nLista de alimentos:")
sistema.mostrar()
