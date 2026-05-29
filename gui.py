import importlib.util
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

import insertion_sort
import listas_simples

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

        self.inventario = listas_simples.ListaInventario()
        self.heap = heap_mod.MinHeapAlimentos()

        self.create_widgets()
        self.log("Sistema listo.")

#---------------------------------------------------------------------------

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Registrar alimento")
        form_frame.place(x=16, y=16, width=420, height=200)

        labels = ["Nombre", "Cantidad"]
        self.entries = {}

        for idx, texto in enumerate(labels):
            ttk.Label(form_frame, text=texto).place(x=10, y=12 + idx * 38)
            entry = ttk.Entry(form_frame)
            entry.place(x=150, y=10 + idx * 38, width=240)
            entry.bind("<Return>", self.agregar_alimento)
            self.entries[texto] = entry

        ttk.Label(form_frame, text="Fecha de vencimiento").place(x=10, y=88)
        self.date_entries = {}

        dia_entry = ttk.Entry(form_frame)
        dia_entry.place(x=150, y=86, width=48)
        dia_entry.bind("<Return>", self.agregar_alimento)
        dia_entry.bind("<KeyRelease>", lambda event: self.limit_entry(event.widget, 2))
        self.date_entries["dia"] = dia_entry

        ttk.Label(form_frame, text="-").place(x=203, y=88)

        mes_entry = ttk.Entry(form_frame)
        mes_entry.place(x=218, y=86, width=48)
        mes_entry.bind("<Return>", self.agregar_alimento)
        mes_entry.bind("<KeyRelease>", lambda event: self.limit_entry(event.widget, 2))
        self.date_entries["mes"] = mes_entry

        ttk.Label(form_frame, text="-").place(x=271, y=88)

        anio_entry = ttk.Entry(form_frame)
        anio_entry.place(x=286, y=86, width=104)
        anio_entry.bind("<Return>", self.agregar_alimento)
        anio_entry.bind("<KeyRelease>", lambda event: self.limit_entry(event.widget, 4))
        self.date_entries["anio"] = anio_entry

        ttk.Button(form_frame, text="Agregar alimento", command=self.agregar_alimento).place(
            x=10, y=142, width=380
        )

        actions_frame = ttk.LabelFrame(self, text="Acciones")
        actions_frame.place(x=16, y=228, width=420, height=268)

        ttk.Button(actions_frame, text="Proximo a vencer", command=self.mostrar_proximo_vencer).place(x=10, y=12, width=190)
        ttk.Button(actions_frame, text="Ordenar por fecha", command=self.ordenar_productos).place(x=220, y=12, width=190)
        ttk.Label(actions_frame, text="Por vencer en").place(x=10, y=102)
        self.days_entry = ttk.Entry(actions_frame)
        self.days_entry.place(x=104, y=100, width=42)
        self.days_entry.insert(0, "7")
        ttk.Label(actions_frame, text="dias").place(x=152, y=102)
        ttk.Button(actions_frame, text="Retirar alimentos", command=self.retirar_por_vencer).place(x=220, y=100, width=190)
        ttk.Label(actions_frame, text="Eliminar alimento").place(x=10, y=146)
        self.delete_entry = ttk.Entry(actions_frame)
        self.delete_entry.place(x=116, y=144, width=98)
        self.delete_entry.bind("<Return>", self.eliminar_alimento)
        ttk.Button(actions_frame, text="Eliminar", command=self.eliminar_alimento).place(x=220, y=144, width=90)
        ttk.Button(actions_frame, text="Limpiar log", command=self.limpiar_log).place(x=10, y=188, width=400)

        self.log_text = ScrolledText(self, wrap=tk.WORD, state="disabled", font=("Consolas", 11))
        self.log_text.place(x=452, y=16, width=424, height=480)


    def log(self, mensaje, limpiar=False, con_hora=True):
        self.log_text.config(state="normal")

        if limpiar:
            self.log_text.delete("1.0", tk.END)

        if isinstance(mensaje, list):
            self.log_text.insert(tk.END, "\n".join(mensaje))
            self.log_text.insert(tk.END, "\n")
        elif mensaje:
            if con_hora:
                mensaje = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}"

            self.log_text.insert(tk.END, f"{mensaje}\n")

        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

#-------------------------------------------------------------------

    def clear_entries(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

        for entry in self.date_entries.values():
            entry.delete(0, tk.END)

    def normalizar_fecha(self, dia, mes, anio):
        if not dia.isdigit() or not mes.isdigit() or not anio.isdigit():
            raise ValueError

        if len(dia) > 2 or len(mes) > 2 or len(anio) != 4:
            raise ValueError

        fecha_convertida = datetime(int(anio), int(mes), int(dia))
        return fecha_convertida.strftime("%Y-%m-%d")

    def limit_entry(self, entry, max_length):
        texto = entry.get()

        if len(texto) > max_length:
            entry.delete(max_length, tk.END)

    def limpiar_log(self):
        self.clear_entries()
        self.delete_entry.delete(0, tk.END)
        self.log("", limpiar=True, con_hora=False)

#------------------------------------------------------------------

    def agregar_alimento(self, event=None):
        nombre = self.entries["Nombre"].get().strip()
        cantidad = self.entries["Cantidad"].get().strip()
        dia = self.date_entries["dia"].get().strip()
        mes = self.date_entries["mes"].get().strip()
        anio = self.date_entries["anio"].get().strip()

        if not nombre or not cantidad or not dia or not mes or not anio:
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        try:
            fecha_normalizada = self.normalizar_fecha(dia, mes, anio)
            producto = self.inventario.insertar(nombre, cantidad, fecha_normalizada)
            self.heap.insertar_alimento(producto)
        except ValueError:
            messagebox.showerror("Dato invalido", "Cantidad numerica y fecha DD-MM-AAAA.")
            return

        self.mostrar_alimentos_agregados()

        self.clear_entries()


    def mostrar_alimentos_agregados(self):
        productos = self.inventario.obtener_productos()
        lineas = ["Alimentos agregados:"]

        for producto in productos:
            lineas.append(
                f"- {producto.nombre} ({producto.cantidad}) - "
                f"vence {producto.fecha_vencimiento.strftime('%Y-%m-%d')}"
            )

        self.log(lineas, limpiar=True, con_hora=False)


    def eliminar_alimento(self):
        nombre = self.delete_entry.get().strip()

        if not nombre:
            messagebox.showwarning("Falta nombre", "Escribe el nombre del alimento a eliminar.")
            return

        eliminado_inventario = self.inventario.eliminar(nombre)

        if not eliminado_inventario:
            self.clear_entries()
            self.log(f"No se encontro el alimento: {nombre}", limpiar=True)
            return

        self.heap.eliminar_alimento(nombre)
        self.mostrar_alimentos_agregados()
        self.delete_entry.delete(0, tk.END)
        self.clear_entries()


    def mostrar_proximo_vencer(self):
        self.clear_entries()
        alimento = self.heap.ver_proximo_vencer()

        if alimento is None:
            self.log("No hay alimentos registrados.", limpiar=True)
            return

        self.log(
            f"Proximo a vencer: {alimento.nombre} - "
            f"vence {alimento.fecha_vencimiento.strftime('%Y-%m-%d')}",
            limpiar=True
        )

    def retirar_por_vencer(self):
        dias = self.days_entry.get().strip()

        if not dias.isdigit() or int(dias) < 0:
            messagebox.showerror("Dato invalido", "Ingresa una cantidad de dias valida.")
            return

        dias = int(dias)
        hoy = datetime.now().date()
        limite = hoy + timedelta(days=dias)
        retirados = self.heap.extraer_por_fecha(limite)

        for retirado in retirados:
            self.inventario.eliminar(retirado.nombre)

        self.clear_entries()

        if not retirados:
            self.log(f"No hay alimentos por vencer en los proximos {dias} dias.", limpiar=True)
            return

        lineas = [f"Alimentos por vencer retirados ({dias} dias):"]

        for alimento in retirados:
            lineas.append(
                f"- {alimento.nombre} ({alimento.cantidad}) - "
                f"vence {alimento.fecha_vencimiento.strftime('%Y-%m-%d')}"
            )

        self.log(lineas, limpiar=True, con_hora=False)

    def ordenar_productos(self):
        self.clear_entries()
        productos = insertion_sort.insertion_sort(self.inventario.obtener_productos())

        if not productos:
            self.log("No hay productos para ordenar.", limpiar=True)
            return

        self.log("Productos ordenados por vencimiento:", limpiar=True)
        for producto in productos:
            self.log(f"{producto.nombre} - {producto.fecha_vencimiento.date()}")

if __name__ == "__main__":
    app = ProyectoGUI()
    app.mainloop()
