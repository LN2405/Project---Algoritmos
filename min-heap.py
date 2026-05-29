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

