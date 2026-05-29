from datetime import datetime

class NodoProducto:
    def __init__(self, nombre, cantidad, fecha_vencimiento):
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.siguiente = None


class ListaInventario:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def insertar(self, nombre, cantidad, fecha_vencimiento):

        nuevo = NodoProducto(nombre, cantidad, fecha_vencimiento)

        if self.inicio is None:
            self.inicio = nuevo
            self.fin = nuevo

        else:
            self.fin.siguiente = nuevo
            self.fin = nuevo

        return nuevo

    def eliminar(self, nombre):

        actual = self.inicio
        anterior = None

        while actual is not None:

            if actual.nombre.lower() == nombre.lower():

                if anterior is None:
                    self.inicio = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente

                if actual == self.fin:
                    self.fin = anterior

                return True

            anterior = actual
            actual = actual.siguiente

        return False

    def obtener_productos(self):

        productos = []
        actual = self.inicio

        while actual is not None:

            productos.append(actual)
            actual = actual.siguiente

        return productos
