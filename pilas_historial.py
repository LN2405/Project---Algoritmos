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

        print(f"Acción registrada: {accion}")

    
    def pop(self):

        if self.tope is None:
            print("No hay acciones en el historial.")
            return None

        accion_eliminada = self.tope.accion

        self.tope = self.tope.siguiente

        print(f"Acción eliminada del historial: {accion_eliminada}")

        return accion_eliminada
    
    def mostrar_historial(self):

        if self.tope is None:
            print("El historial está vacío.")
            return

        print("\n=== HISTORIAL DE ACCIONES ===")

        actual = self.tope

       
        while actual is not None:
            print("-", actual.accion)
            actual = actual.siguiente

historial = PilaHistorial()
historial.push("Se agregó Leche")
historial.push("Se donó Pan")
historial.push("Se eliminó Yogurt")
historial.mostrar_historial()
historial.pop()
historial.mostrar_historial()