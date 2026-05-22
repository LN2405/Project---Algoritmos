# ==========================================
# PILA DE HISTORIAL DE ACCIONES
# Proyecto: Sistema de Control de Desperdicio de Alimentos
# ODS 12 - Producción y consumo responsables
# ==========================================


# ------------------------------------------
# Clase Nodo
# Cada nodo guarda una acción del historial
# y una referencia al siguiente nodo.
# ------------------------------------------

class Nodo:
    def __init__(self, accion):
        self.accion = accion      # Guarda el texto de la acción
        self.siguiente = None     # Apunta al siguiente nodo


# ------------------------------------------
# Clase PilaHistorial
# Implementa una pila usando nodos enlazados
#
# La pila funciona con la lógica:
# "Último en entrar, primero en salir"
# (LIFO - Last In First Out)
# ------------------------------------------

class PilaHistorial:
    
    def __init__(self):
        self.tope = None  # El tope es el último elemento agregado

    
    # --------------------------------------
    # push()
    # Agrega una nueva acción al historial
    # --------------------------------------
    
    def push(self, accion):
        
        # Crear un nuevo nodo con la acción
        nuevo = Nodo(accion)

        # El nuevo nodo apunta al nodo actual del tope
        nuevo.siguiente = self.tope

        # Ahora el nuevo nodo se convierte en el tope
        self.tope = nuevo

        print(f"Acción registrada: {accion}")


    # --------------------------------------
    # pop()
    # Elimina la última acción registrada
    # --------------------------------------
    
    def pop(self):

        # Verificar si la pila está vacía
        if self.tope is None:
            print("No hay acciones en el historial.")
            return None

        # Guardar la acción que se eliminará
        accion_eliminada = self.tope.accion

        # El tope avanza al siguiente nodo
        self.tope = self.tope.siguiente

        print(f"Acción eliminada del historial: {accion_eliminada}")

        return accion_eliminada


    # --------------------------------------
    # mostrar_historial()
    # Muestra todas las acciones guardadas
    # desde la más reciente hasta la más antigua
    # --------------------------------------
    
    def mostrar_historial(self):

        # Verificar si la pila está vacía
        if self.tope is None:
            print("El historial está vacío.")
            return

        print("\n=== HISTORIAL DE ACCIONES ===")

        actual = self.tope

        # Recorrer toda la pila
        while actual is not None:
            print("-", actual.accion)
            actual = actual.siguiente


# ==========================================
# EJEMPLO DE USO
# ==========================================

# Crear la pila del historial
historial = PilaHistorial()


# Registrar acciones del sistema
historial.push("Se agregó Leche")
historial.push("Se donó Pan")
historial.push("Se eliminó Yogurt")


# Mostrar historial
historial.mostrar_historial()


# Eliminar la última acción registrada
historial.pop()


# Mostrar historial actualizado
historial.mostrar_historial()