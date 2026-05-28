import importlib.util
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import insertion_sort
import listas_dobles
import pilas_historial

RUTA_HEAP = os.path.join(os.path.dirname(__file__), "min-heap.py")
SPEC_HEAP = importlib.util.spec_from_file_location("min_heap", RUTA_HEAP)
heap_mod = importlib.util.module_from_spec(SPEC_HEAP)
SPEC_HEAP.loader.exec_module(heap_mod)


class ProyectoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Desperdicio de Alimentos")
        self.geometry("900x520")
        self.resizable(False, False)

        self.inventario = listas_dobles.ListaInventario()
        self.heap = heap_mod.MinHeapAlimentos()
        self.historial = pilas_historial.PilaHistorial()

        self.create_widgets()
        self.log("Sistema listo.")

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Registrar alimento")
        form_frame.place(x=16, y=16, width=420, height=220)

        labels = ["Nombre", "Cantidad", "Lugar", "Fecha de vencimiento"]
        self.entries = {}

        for idx, texto in enumerate(labels):
            ttk.Label(form_frame, text=texto).place(x=10, y=12 + idx * 42)
            entry = ttk.Entry(form_frame)
            entry.place(x=150, y=10 + idx * 42, width=240)
            entry.bind("<Return>", self.add_food)
            self.entries[texto] = entry

        ttk.Button(form_frame, text="Agregar alimento", command=self.add_food).place(
            x=10, y=180, width=380
        )

        actions_frame = ttk.LabelFrame(self, text="Acciones")
        actions_frame.place(x=16, y=248, width=420, height=248)

        ttk.Button(actions_frame, text="Proximo a vencer", command=self.show_next).place(x=10, y=12, width=190)
        ttk.Button(actions_frame, text="Listar heap", command=self.show_heap).place(x=220, y=12, width=190)
        ttk.Button(actions_frame, text="Ordenar por fecha", command=self.sort_products).place(x=10, y=56, width=190)
        ttk.Button(actions_frame, text="Mostrar historial", command=self.show_history).place(x=220, y=56, width=190)
        ttk.Button(actions_frame, text="Quitar accion", command=self.pop_history).place(x=10, y=100, width=400)
        ttk.Button(actions_frame, text="Limpiar log", command=self.clear_log).place(x=10, y=144, width=400)

        self.log_text = ScrolledText(self, wrap=tk.WORD, state="disabled", font=("Consolas", 11))
        self.log_text.place(x=452, y=16, width=424, height=480)

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def clear_log_text(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")

    def prepare_action_view(self):
        self.clear_entries()
        self.clear_log_text()

    def add_food(self, event=None):
        nombre = self.entries["Nombre"].get().strip()
        cantidad = self.entries["Cantidad"].get().strip()
        lugar = self.entries["Lugar"].get().strip()
        fecha = self.entries["Fecha de vencimiento"].get().strip()

        if not nombre or not cantidad or not lugar or not fecha:
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        try:
            self.inventario.insertar(nombre, cantidad, lugar, fecha)
            self.heap.insertar_alimento(nombre, cantidad, lugar, fecha)
        except ValueError:
            messagebox.showerror("Dato invalido", "Cantidad numerica y fecha AAAA-MM-DD.")
            return

        self.historial.push(f"Agregado alimento {nombre} ({cantidad})")
        self.log(f"Alimento agregado: {nombre} ({cantidad}) - vence {fecha} en {lugar}")

        self.clear_entries()

    def show_next(self):
        self.prepare_action_view()
        alimento = self.heap.ver_proximo_vencer()

        if alimento is None:
            self.log("No hay alimentos registrados.")
            return

        self.log(
            f"Proximo a vencer: {alimento['nombre']} - "
            f"vence {alimento['fecha'].strftime('%Y-%m-%d')} ({alimento['lugar']})"
        )

    def show_heap(self):
        self.prepare_action_view()
        alimentos = self.heap.mostrar()

        if not alimentos:
            self.log("Heap vacio.")
            return

        self.log("Alimentos en heap:")
        for alimento in alimentos:
            self.log(alimento)

    def sort_products(self):
        self.prepare_action_view()
        productos = insertion_sort.insertion_sort(self.inventario.obtener_productos())

        if not productos:
            self.log("No hay productos para ordenar.")
            return

        self.log("Productos ordenados por vencimiento:")
        for producto in productos:
            self.log(f"{producto.nombre} - {producto.fecha_vencimiento.date()}")

    def show_history(self):
        self.prepare_action_view()
        acciones = self.historial.mostrar()

        if not acciones:
            self.log("Historial vacio.")
            return

        self.log("Historial de acciones:")
        for accion in acciones:
            self.log(f"- {accion}")

    def pop_history(self):
        self.prepare_action_view()
        accion = self.historial.pop()

        if accion is None:
            self.log("No hay accion para quitar.")
        else:
            self.log(f"Accion eliminada: {accion}")

    def clear_log(self):
        self.clear_entries()
        self.clear_log_text()

    def log(self, mensaje):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")


if __name__ == "__main__":
    app = ProyectoGUI()
    app.mainloop()
