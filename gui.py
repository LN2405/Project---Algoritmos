import importlib.util
import io
import os
import sys
from contextlib import redirect_stdout
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

BASE_DIR = os.path.dirname(__file__)


def load_module_from_path(name, filename):
    path = os.path.join(BASE_DIR, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    with redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module

try:
    insertion_mod = load_module_from_path("insertion_sort_module", "insertion_sort.py")
    heap_mod = load_module_from_path("min_heap_module", "min-heap.py")
    historial_mod = load_module_from_path("pilas_historial_module", "pilas_historial.py")
except Exception as exc:
    print("No se pudo cargar uno o más módulos del proyecto:", exc)
    sys.exit(1)


class SortProducto:
    def __init__(self, nombre, fecha_vencimiento):
        self.nombre = nombre
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")

    def __repr__(self):
        return f"{self.nombre} - {self.fecha_vencimiento.date()}"


class ProyectoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Desperdicio de Alimentos")
        self.geometry("900x520")
        self.resizable(False, False)

        self.heap = heap_mod.MinHeapAlimentos()
        self.historial = historial_mod.PilaHistorial()
        self.sort_items = []

        self.create_widgets()
        self.log("Interfaz lista. Registra alimentos y usa heap e historial.")

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Registrar alimento")
        form_frame.place(x=16, y=16, width=420, height=220)

        labels = ["Nombre", "Cantidad", "Lugar", "Fecha de vencimiento"]
        self.entries = {}
        for idx, label_text in enumerate(labels):
            label = ttk.Label(form_frame, text=label_text)
            label.place(x=10, y=12 + idx * 42)
            entry = ttk.Entry(form_frame)
            entry.place(x=150, y=10 + idx * 42, width=240)
            self.entries[label_text] = entry

        boton_agregar = ttk.Button(form_frame, text="Agregar alimento", command=self.add_food)
        boton_agregar.place(x=10, y=180, width=380)

        actions_frame = ttk.LabelFrame(self, text="Acciones")
        actions_frame.place(x=16, y=248, width=420, height=248)

        ttk.Button(actions_frame, text="Próximo a vencer", command=self.show_next).place(x=10, y=12, width=190)
        ttk.Button(actions_frame, text="Listar heap", command=self.show_heap).place(x=220, y=12, width=190)
        ttk.Button(actions_frame, text="Ordenar por fecha", command=self.sort_products).place(x=10, y=56, width=190)
        ttk.Button(actions_frame, text="Mostrar historial", command=self.show_history).place(x=220, y=56, width=190)
        ttk.Button(actions_frame, text="Quitar acción", command=self.pop_history).place(x=10, y=100, width=400)
        ttk.Button(actions_frame, text="Limpiar log", command=lambda: self.log_text.delete("1.0", tk.END)).place(x=10, y=144, width=400)

        self.log_text = ScrolledText(self, wrap=tk.WORD, state="disabled", font=("Consolas", 11))
        self.log_text.place(x=452, y=16, width=424, height=480)

    def log(self, mensaje):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def add_food(self):
        nombre = self.entries["Nombre"].get().strip()
        cantidad = self.entries["Cantidad"].get().strip()
        lugar = self.entries["Lugar"].get().strip()
        fecha = self.entries["Fecha de vencimiento"].get().strip()

        if not nombre or not cantidad or not lugar or not fecha:
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        try:
            cantidad = int(cantidad)
        except ValueError:
            messagebox.showerror("Valor inválido", "La cantidad debe ser un número entero.")
            return

        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Formato inválido", "La fecha debe ser AAAA-MM-DD.")
            return

        self.heap.insertar_alimento(nombre, cantidad, lugar, fecha)
        self.sort_items.append(SortProducto(nombre, fecha))
        self.historial.push(f"Agregado alimento {nombre} ({cantidad})")
        self.log(f"Alimento agregado: {nombre} ({cantidad}) - vence {fecha} en {lugar}")
        self.clear_fields()

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def show_next(self):
        proximo = self.heap.ver_proximo_vencer()
        if proximo is None:
            self.log("No hay alimentos registrados.")
        elif isinstance(proximo, str):
            self.log(proximo)
        else:
            self.log(f"Próximo a vencer: {proximo['nombre']} - vence {proximo['fecha'].strftime('%Y-%m-%d')} ({proximo['lugar']})")

    def show_heap(self):
        if not self.heap.heap:
            self.log("Heap vacío.")
            return
        self.log("Alimentos en heap:")
        for item in self.heap.heap:
            self.log(f"{item['nombre']} ({item['cantidad']}) - vence {item['fecha'].strftime('%Y-%m-%d')} en {item['lugar']}")

    def sort_products(self):
        if not self.sort_items:
            self.log("No hay productos para ordenar.")
            return
        ordenados = insertion_mod.insertion_sort(self.sort_items)
        self.log("Productos ordenados por vencimiento:")
        for producto in ordenados:
            self.log(f"{producto.nombre} - {producto.fecha_vencimiento.date()}")

    def show_history(self):
        historial = self.historial.mostrar()
        if not historial:
            self.log("Historial vacío.")
            return
        self.log("Historial de acciones:")
        for accion in historial:
            self.log(f"- {accion}")

    def pop_history(self):
        accion = self.historial.pop()
        if accion is None:
            self.log("No hay acción para quitar.")
        else:
            self.log(f"Acción eliminada: {accion}")


if __name__ == "__main__":
    app = ProyectoGUI()
    app.mainloop()
