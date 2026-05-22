class Residuonodo:
    """Nodo que representa un residuo individual en la planta."""
    def __init__(self, id_residuo, tipo, peso, impacto_ambiental):
        self.id_residuo = id_residuo        # Ej: 101, 102
        self.tipo = tipo                    # Ej: "Plástico", "Vidrio", "Cartón"
        self.peso = peso                    # En kilogramos
        self.impacto_ambiental = impacto_ambiental  # Escala 1-10 (Prioridad de contaminación)
        
        # Punteros de la lista doblemente enlazada
        self.next = None
        self.prev = None

class ListaResiduos:
    """Lista doblemente enlazada para gestionar el inventario dinámico de reciclaje."""
    def __init__(self):
        self.head = None
        self.tail = None

    def insertar_al_final(self, id_residuo, tipo, peso, impacto):
        """Registra un nuevo residuo que entra a la planta (O(1))."""
        nuevo_nodo = Residuonodo(id_residuo, tipo, peso, impacto)
        if not self.head:
            self.head = nuevo_nodo
            self.tail = nuevo_nodo
        else:
            self.tail.next = nuevo_nodo
            nuevo_nodo.prev = self.tail
            self.tail = nuevo_nodo

    def mostrar_inventario_adelante(self):
        """Recorre la lista desde el primer residuo ingresado al último."""
        residuos = []
        current = self.head
        while current:
            residuos.append(f"[{current.id_residuo}] {current.tipo} ({current.peso}kg) - Impacto: {current.impacto_ambiental}/10")
            current = current.next
        return residuos

    def eliminar_por_id(self, id_residuo):
        """Elimina un residuo cuando ya fue procesado/reciclado."""
        current = self.head
        
        while current:
            if current.id_residuo == id_residuo:
                # Caso 1: Es el único nodo en la lista
                if current == self.head and current == self.tail:
                    self.head = None
                    self.tail = None
                # Caso 2: Es la cabeza (el primero)
                elif current == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                # Caso 3: Es la cola (el último)
                elif current == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None
                # Caso 4: Está en el medio
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return True # Eliminado con éxito
            current = current.next
        return False # No se encontró

    # --- MÉTODOS AVANZADOS (Para ganar puntos con el profesor) ---

    def calcular_peso_total_por_tipo(self, tipo_buscado):
        """Recorre la lista y suma el peso de un tipo específico de residuo."""
        total_peso = 0.0
        current = self.head
        while current:
            if current.tipo.lower() == tipo_buscado.lower():
                total_peso += current.peso
            current = current.next
        return total_peso

    def filtrar_alta_contaminacion(self, umbral=7):
        """Retorna una lista de ID de residuos que superan un umbral de impacto."""
        criticos = []
        current = self.head
        while current:
            if current.impacto_ambiental >= umbral:
                criticos.append(current.id_residuo)
            current = current.next
        return criticos

