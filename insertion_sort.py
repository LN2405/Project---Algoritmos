from datetime import datetime

class Producto:
    def __init__(self, nombre, vencimiento):
        self.nombre = nombre
        self.vencimiento = datetime.strptime(vencimiento, "%Y-%m-%d")

    def mostrar(self):
        return f"{self.nombre} - {self.vencimiento.date()}"


def insertion_sort(productos):

    productos_ordenados = productos.copy()

    for i in range(1, len(productos_ordenados)):

        actual = productos_ordenados[i]
        j = i - 1

        while j >= 0 and productos_ordenados[j].vencimiento > actual.vencimiento:

            productos_ordenados[j + 1] = productos_ordenados[j]
            j -= 1

        productos_ordenados[j + 1] = actual

    return productos_ordenados


productos = [
    Producto("Leche", "2026-05-30"),
    Producto("Pan", "2026-05-24"),
    Producto("Yogurt", "2026-05-22"),
    Producto("Queso", "2026-06-01")
]

ordenados = insertion_sort(productos)

print("Productos ordenados por vencimiento:\n")

for producto in ordenados:
    print(producto.mostrar())