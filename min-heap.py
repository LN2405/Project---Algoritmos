from datetime import datetime

class MinHeapAlimentos:

    def __init__(self):
        self.heap = []

    # Padre
    def parent(self, index):
        return (index - 1) // 2

    # Hijo izquierdo
    def left_child(self, index):
        return 2 * index + 1

    # Hijo derecho
    def right_child(self, index):
        return 2 * index + 2

    # Insertar alimento
    def insertar_alimento(self, nombre, cantidad, lugar, fecha_vencimiento):

        # Convertimos la fecha a objeto datetime
        fecha = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")

        alimento = {
            "nombre": nombre,
            "cantidad": cantidad,
            "lugar": lugar,
            "fecha": fecha
        }

        self.heap.append(alimento)
        self.heapify_up(len(self.heap) - 1)

    # Subir elemento
    def heapify_up(self, index):

        while index > 0:

            parent = self.parent(index)

            # Comparar fechas
            if self.heap[index]["fecha"] < self.heap[parent]["fecha"]:

                self.heap[index], self.heap[parent] = \
                self.heap[parent], self.heap[index]

                index = parent

            else:
                break

    # Mostrar alimento más urgente
    def ver_proximo_vencer(self):

        if not self.heap:
            return "No hay alimentos registrados"

        return self.heap[0]

    # Extraer alimento más urgente
    def extraer_proximo_vencer(self):

        if not self.heap:
            return "Heap vacío"

        if len(self.heap) == 1:
            return self.heap.pop()

        raiz = self.heap[0]

        self.heap[0] = self.heap.pop()

        self.heapify_down(0)

        return raiz

    # Reordenar hacia abajo
    def heapify_down(self, index):

        size = len(self.heap)

        while self.left_child(index) < size:

            smallest = index

            left = self.left_child(index)
            right = self.right_child(index)

            if left < size and \
            self.heap[left]["fecha"] < self.heap[smallest]["fecha"]:

                smallest = left

            if right < size and \
            self.heap[right]["fecha"] < self.heap[smallest]["fecha"]:

                smallest = right

            if smallest != index:

                self.heap[index], self.heap[smallest] = \
                self.heap[smallest], self.heap[index]

                index = smallest

            else:
                break

    # Mostrar heap
    def mostrar(self):

        for alimento in self.heap:
            print(
                alimento["nombre"],
                "- vence:",
                alimento["fecha"].strftime("%Y-%m-%d")
            )

sistema = MinHeapAlimentos()

sistema.insertar_alimento(
    "Leche",
    20,
    "Supermercado Plaza",
    "2026-05-25"
)

sistema.insertar_alimento(
    "Pan",
    15,
    "Restaurante Sol",
    "2026-05-20"
)

sistema.insertar_alimento(
    "Queso",
    10,
    "Market Food",
    "2026-05-22"
)

print("Alimento que vencerá primero:")
print(sistema.ver_proximo_vencer())