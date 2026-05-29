from datetime import datetime

class MinHeapAlimentos:

    def __init__(self):
        self.heap = []

    # Registrar alimento
    def insertar_alimento(self, nombre, cantidad, lugar, fecha_vencimiento):

        # Convertir texto a fecha
        fecha = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")

        alimento = {
            "nombre": nombre,
            "cantidad": cantidad,
            "lugar": lugar,
            "fecha": fecha
        }

        # Insertar al final
        self.heap.append(alimento)

        # Reordenar heap
        self.heapify_up(len(self.heap) - 1)

    # Reordenar hacia arriba
    def heapify_up(self, index):

        while index > 0:

            # Fórmula del padre
            parent = (index - 1) // 2

            # Comparar fechas
            if self.heap[index]["fecha"] < self.heap[parent]["fecha"]:

                # Intercambiar
                self.heap[index], self.heap[parent] = \
                self.heap[parent], self.heap[index]

                # Seguir subiendo
                index = parent

            else:
                break

    # Ver alimento que vencerá primero
    def ver_proximo_vencer(self):

        if not self.heap:
            return "No hay alimentos registrados"

        return self.heap[0]

    # Mostrar todos los alimentos
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

