class MinHeapAlimentos:

    def __init__(self):
        self.heap = []

    def insertar_alimento(self, producto):

        self.heap.append(producto)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, index):

        while index > 0:

            parent = (index - 1) // 2

            if self.heap[index].fecha_vencimiento < self.heap[parent].fecha_vencimiento:

                self.heap[index], self.heap[parent] = (
                    self.heap[parent],
                    self.heap[index]
                )

                index = parent

            else:
                break

    def heapify_down(self, index):

        size = len(self.heap)

        while True:

            menor = index
            izquierdo = 2 * index + 1
            derecho = 2 * index + 2

            if izquierdo < size and self.heap[izquierdo].fecha_vencimiento < self.heap[menor].fecha_vencimiento:
                menor = izquierdo

            if derecho < size and self.heap[derecho].fecha_vencimiento < self.heap[menor].fecha_vencimiento:
                menor = derecho

            if menor == index:
                break

            self.heap[index], self.heap[menor] = self.heap[menor], self.heap[index]
            index = menor

    def eliminar_alimento(self, nombre):

        for index, alimento in enumerate(self.heap):

            if alimento.nombre.lower() == nombre.lower():

                self.heap[index] = self.heap[-1]
                self.heap.pop()

                if index < len(self.heap):
                    self.heapify_down(index)
                    self.heapify_up(index)

                return True

        return False

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

    def extraer_por_fecha(self, fecha_limite):

        retirados = []

        while True:
            alimento = self.ver_proximo_vencer()

            if alimento is None:
                break

            fecha_alimento = alimento.fecha_vencimiento.date()

            if fecha_alimento > fecha_limite:
                break

            retirados.append(self.extraer_proximo_vencer())
 
        return retirados


