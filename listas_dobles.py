from datetime import datetime


class Producto:
    def __init__(self, nombre, cantidad, lugar, fecha_vencimiento):
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.lugar = lugar
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")


class NodoProducto:
    def __init__(self, producto):
        self.producto = producto
        self.siguiente = None
        self.anterior = None


class ListaInventario:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def insertar(self, nombre, cantidad, lugar, fecha_vencimiento):

        producto = Producto(nombre, cantidad, lugar, fecha_vencimiento)
        nuevo = NodoProducto(producto)

        if self.inicio is None:
            self.inicio = nuevo
            self.fin = nuevo

        else:
            self.fin.siguiente = nuevo
            nuevo.anterior = self.fin
            self.fin = nuevo

    def eliminar(self, nombre):

        actual = self.inicio

        while actual is not None:

            if actual.producto.nombre.lower() == nombre.lower():

                if actual == self.inicio and actual == self.fin:
                    self.inicio = None
                    self.fin = None

                elif actual == self.inicio:
                    self.inicio = actual.siguiente
                    self.inicio.anterior = None

                elif actual == self.fin:
                    self.fin = actual.anterior
                    self.fin.siguiente = None

                else:
                    actual.anterior.siguiente = actual.siguiente
                    actual.siguiente.anterior = actual.anterior

                return True

            actual = actual.siguiente

        return False

    def mostrar(self):

        actual = self.inicio

        while actual is not None:

            producto = actual.producto

            print(
                f"{producto.nombre} - "
                f"{producto.fecha_vencimiento.date()}"
            )

            actual = actual.siguiente
