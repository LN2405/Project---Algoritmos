class Nodo:
    def __init__(self, accion):
        self.accion = accion
        self.siguiente = None


class PilaHistorial:
    def __init__(self):
        self.tope = None

    def push(self, accion):
        nuevo = Nodo(accion)
        nuevo.siguiente = self.tope
        self.tope = nuevo

    def pop(self):
        if self.tope is None:
            return None

        accion = self.tope.accion
        self.tope = self.tope.siguiente
        return accion

    def mostrar(self):
        acciones = []
        actual = self.tope

        while actual is not None:
            acciones.append(actual.accion)
            actual = actual.siguiente

        return acciones
