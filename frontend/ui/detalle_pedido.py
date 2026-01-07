# import tkinter as tk
# from tkinter import ttk, messagebox
# from api.type import get, post, delete

# class DetallePedidoTab:
#     endpoint = "/detalle-pedidos"

#     def __init__(self, notebook):
#         self.frame = ttk.Frame(notebook)
#         notebook.add(self.frame, text="Detalle Pedidos")

#         self.form = {}
#         self._build_form()
#         self._build_buttons()
#         self._build_table()
#         self.load()

#     def _build_form(self):
#         form_frame = ttk.LabelFrame(self.frame, text="Formulario Detalle Pedido", padding=10)
#         form_frame.pack(fill="x", padx=10, pady=10)

#         labels = [
#             ("id_pedido", "ID Pedido"),
#             ("cantidad", "Cantidad"),
#             ("precio_unitario", "Precio Unitario")
#         ]

#         for i, (key, label) in enumerate(labels):
#             ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w")
#             entry = ttk.Entry(form_frame)
#             entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
#             self.form[key] = entry

#         form_frame.columnconfigure(1, weight=1)

#     def _build_buttons(self):
#         btn_frame = ttk.Frame(self.frame)
#         btn_frame.pack(fill="x", padx=10, pady=5)
#         ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

#     def _build_table(self):
#         columns = ("ID Detalle", "ID Pedido", "Cantidad", "Precio Unitario")
#         self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
#         for col in columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=120)
#         self.tree.pack(fill="both", expand=True, padx=10, pady=10)
#         self.tree.bind("<Double-1>", self.on_double_click)

#     def load(self):
#         try:
#             res = get(self.endpoint)
#             res.raise_for_status()
#             data = res.json()
#         except Exception as e:
#             messagebox.showerror("Error", f"No se pudieron cargar detalles: {e}")
#             return

#         self.tree.delete(*self.tree.get_children())
#         for d in data:
#             self.tree.insert("", "end", values=(
#                 d.get("id_detalle_pedido"),
#                 d.get("id_pedido"),
#                 d.get("cantidad"),
#                 d.get("precio_unitario")
#             ))

#     def clear(self):
#         for entry in self.form.values():
#             entry.delete(0, "end")
#         for sel in self.tree.selection():
#             self.tree.selection_remove(sel)

#     def _collect_form(self):
#         return {k: v.get().strip() for k, v in self.form.items()}

#     def validate(self, data):
#         # Validaciones
#         try:
#             cantidad = int(data["cantidad"])
#             if cantidad <= 0:
#                 raise ValueError("Cantidad debe ser mayor a 0")
#         except ValueError:
#             messagebox.showerror("Error", "Cantidad debe ser un número entero mayor a 0")
#             return False

#         try:
#             precio = float(data["precio_unitario"])
#             if precio < 0:
#                 raise ValueError("Precio Unitario no puede ser negativo")
#         except ValueError:
#             messagebox.showerror("Error", "Precio Unitario debe ser un número mayor o igual a 0")
#             return False

#         try:
#             id_pedido = int(data["id_pedido"])
#             if id_pedido <= 0:
#                 raise ValueError()
#         except ValueError:
#             messagebox.showerror("Error", "ID Pedido debe ser un número válido")
#             return False

#         return True

#     def create(self):
#         data = self._collect_form()
#         if not self.validate(data):
#             return
#         # Convertir tipos
#         data = {
#             "id_pedido": int(data["id_pedido"]),
#             "cantidad": int(data["cantidad"]),
#             "precio_unitario": float(data["precio_unitario"])
#         }
#         try:
#             res = post(self.endpoint, data)
#             res.raise_for_status()
#         except Exception as e:
#             messagebox.showerror("Error", f"No se pudo crear detalle: {e}")
#             return
#         self.clear()
#         self.load()

#     def get_selected_id(self):
#         sel = self.tree.selection()
#         if not sel:
#             return None
#         return self.tree.item(sel[0])["values"][0]

#     def delete_selected(self):
#         id_ = self.get_selected_id()
#         if not id_:
#             messagebox.showwarning("Aviso", "Selecciona un detalle para eliminar")
#             return
#         if not messagebox.askyesno("Confirmar", "¿Eliminar el detalle seleccionado?"):
#             return
#         try:
#             res = delete(f"{self.endpoint}/{id_}")
#             res.raise_for_status()
#         except Exception as e:
#             messagebox.showerror("Error", f"No se pudo eliminar detalle: {e}")
#             return
#         self.clear()
#         self.load()

#     def on_double_click(self, event):
#         sel = self.tree.selection()
#         if not sel:
#             return
#         item = self.tree.item(sel[0])["values"]
#         keys = ["id_detalle_pedido", "id_pedido", "cantidad", "precio_unitario"]
#         values = dict(zip(keys, item))
#         for k in ("id_pedido", "cantidad", "precio_unitario"):
#             self.form[k].delete(0, "end")
#             self.form[k].insert(0, values.get(k, ""))
import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class DetallePedidoTab:
    endpoint = "/detalle-pedidos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Detalle Pedidos")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Detalle Pedido", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [
            ("id_pedido", "ID Pedido"),
            ("cantidad", "Cantidad"),
            ("precio_unitario", "Precio Unitario")
        ]

        for i, (key, label) in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.form[key] = entry

        form_frame.columnconfigure(1, weight=1)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

    def _build_table(self):
        columns = ("ID Detalle", "ID Pedido", "Cantidad", "Precio Unitario")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar detalles: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for d in data:
            self.tree.insert("", "end", values=(
                d.get("id_detalle_pedido"),
                d.get("id_pedido"),
                d.get("cantidad"),
                d.get("precio_unitario")
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        return {k: v.get().strip() for k, v in self.form.items()}

    def validate(self, data):
        try:
            cantidad = int(data["cantidad"])
            if cantidad <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero mayor a 0")
            return False

        try:
            precio = float(data["precio_unitario"])
            if precio < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Precio Unitario debe ser un número mayor o igual a 0")
            return False

        try:
            id_pedido = int(data["id_pedido"])
            if id_pedido <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "ID Pedido debe ser un número válido")
            return False

        return True

    def create(self):
        data = self._collect_form()
        if not self.validate(data):
            return

        payload = {
            "id_pedido": int(data["id_pedido"]),
            "cantidad": int(data["cantidad"]),
            "precio_unitario": float(data["precio_unitario"])
        }

        try:
            res = post(self.endpoint, payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear detalle: {e}")
            return

        self.clear()
        self.load()

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def update_selected(self):
        id_detalle = self.get_selected_id()
        if not id_detalle:
            messagebox.showwarning("Aviso", "Selecciona un detalle para actualizar")
            return

        data = self._collect_form()
        if not self.validate(data):
            return

        payload = {
            "id_pedido": int(data["id_pedido"]),
            "cantidad": int(data["cantidad"]),
            "precio_unitario": float(data["precio_unitario"])
        }

        try:
            res = put(f"{self.endpoint}/{id_detalle}", payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar detalle: {e}")
            return

        self.clear()
        self.load()

    def delete_selected(self):
        id_detalle = self.get_selected_id()
        if not id_detalle:
            messagebox.showwarning("Aviso", "Selecciona un detalle para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el detalle seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_detalle}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar detalle: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        keys = ["id_detalle_pedido", "id_pedido", "cantidad", "precio_unitario"]
        values = dict(zip(keys, item))
        for k in ("id_pedido", "cantidad", "precio_unitario"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))
