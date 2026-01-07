import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete
from datetime import date

class PedidosClienteTab:
    endpoint = "/pedidos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Pedidos Clientes")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Pedido", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [("id_cliente", "ID Cliente"), ("cantidad_producto", "Cantidad Producto")]
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
        columns = ("ID", "Cliente", "Fecha", "Cantidad", "Estado")
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
            messagebox.showerror("Error", f"No se pudieron cargar pedidos: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for p in data:
            self.tree.insert("", "end", values=(
                p.get("id_pedido"),
                p.get("id_cliente"),
                p.get("fecha"),
                p.get("cantidad_producto"),
                p.get("id_estado")
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        try:
            return {
                "id_cliente": int(self.form["id_cliente"].get()),
                "cantidad_producto": int(self.form["cantidad_producto"].get()),
                "fecha": date.today().isoformat(),
                "tipo_entrega": False,
                "tipo_pedido": False,
                "id_pago": 1,
                "id_estado": 1
            }
        except ValueError:
            return None

    def validate(self, data):
        if not data:
            messagebox.showerror("Error", "ID Cliente y Cantidad deben ser números")
            return False
        if data["cantidad_producto"] <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return False
        if data["id_cliente"] <= 0:
            messagebox.showerror("Error", "ID Cliente debe ser positivo")
            return False
        return True

    def create(self):
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = post(self.endpoint, data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear pedido: {e}")
            return
        self.clear()
        self.load()

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def update_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un pedido para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar pedido: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un pedido para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el pedido seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar pedido: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        keys = ["id_pedido", "id_cliente", "fecha", "cantidad_producto", "id_estado"]
        values = dict(zip(keys, item))
        for k in ("id_cliente", "cantidad_producto"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))


# from ui.base_crud import BaseCRUD
# from api.type import get, post
# from datetime import date

# class PedidosClienteTab(BaseCRUD):
#     endpoint = "/pedidos"
#     columns = ("ID", "Cliente", "Fecha", "Cantidad", "Estado")
#     fields = ("id_cliente", "cantidad_producto")

#     def __init__(self, notebook):
#         super().__init__(notebook, "Pedidos Clientes")

#     def load(self):
#         self.tree.delete(*self.tree.get_children())
#         for p in get(self.endpoint).json():
#             self.tree.insert("", "end", values=(
#                 p["id_pedido"],
#                 p["id_cliente"],
#                 p["fecha"],
#                 p["cantidad_producto"],
#                 p["id_estado"]
#             ))

#     def save(self):
#         data = {
#             "id_cliente": int(self.form["id_cliente"].get()),
#             "cantidad_producto": int(self.form["cantidad_producto"].get()),
#             "fecha": date.today().isoformat(),
#             "tipo_entrega": False,
#             "tipo_pedido": False,
#             "id_pago": 1,
#             "id_estado": 1
#         }
#         post(self.endpoint, data)
#         self.clear()
#         self.load()
