class PilaHistorial:
    def __init__(self):
        self._stack = []

    def push(self, accion):
        self._stack.append(accion)

    def pop(self):
        if not self._stack:
            return None
        return self._stack.pop()

    def mostrar(self):
        return list(reversed(self._stack))
