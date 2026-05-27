from datetime import datetime


class MinHeapAlimentos:
    def __init__(self):
        self.heap = []

    def insertar_alimento(self, nombre, cantidad, lugar, fecha_vencimiento):
        alimento = {
            "nombre": nombre,
            "cantidad": int(cantidad),
            "lugar": lugar,
            "fecha": datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        }

        self.heap.append(alimento)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):
        while index > 0:
            padre = (index - 1) // 2

            if self.heap[index]["fecha"] < self.heap[padre]["fecha"]:
                self.heap[index], self.heap[padre] = self.heap[padre], self.heap[index]
                index = padre
            else:
                break

    def ver_proximo_vencer(self):
        if not self.heap:
            return None

        return self.heap[0]

    def extraer_proximo_vencer(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        raiz = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down(0)
        return raiz

    def heapify_down(self, index):
        size = len(self.heap)

        while True:
            menor = index
            izquierdo = 2 * index + 1
            derecho = 2 * index + 2

            if izquierdo < size and self.heap[izquierdo]["fecha"] < self.heap[menor]["fecha"]:
                menor = izquierdo

            if derecho < size and self.heap[derecho]["fecha"] < self.heap[menor]["fecha"]:
                menor = derecho

            if menor == index:
                break

            self.heap[index], self.heap[menor] = self.heap[menor], self.heap[index]
            index = menor

    def mostrar(self):
        alimentos = []

        for alimento in self.heap:
            alimentos.append(
                f"{alimento['nombre']} ({alimento['cantidad']}) - "
                f"vence {alimento['fecha'].strftime('%Y-%m-%d')} en {alimento['lugar']}"
            )

        return alimentos
