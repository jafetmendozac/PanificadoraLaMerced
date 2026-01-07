import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class ProductosTab:
    endpoint = "/productos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Productos")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Producto", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [("nombre_producto", "Nombre"), ("precio_unitario", "Precio"), ("cantidad_producto", "Cantidad"), ("id_insumos", "ID Insumo")]
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
        columns = ("ID", "Producto", "Precio", "Cantidad", "ID Insumo")
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
            messagebox.showerror("Error", f"No se pudieron cargar productos: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for p in data:
            self.tree.insert("", "end", values=(
                p.get("id_producto"),
                str(p.get("nombre_producto", "")),
                str(p.get("precio_unitario", "")),
                str(p.get("cantidad_producto", "")),
                str(p.get("id_insumos", ""))
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        try:
            return {
                "nombre_producto": self.form["nombre_producto"].get().strip(),
                "precio_unitario": float(self.form["precio_unitario"].get()),
                "cantidad_producto": int(self.form["cantidad_producto"].get()),
                "id_insumos": int(self.form["id_insumos"].get())
            }
        except ValueError:
            return None

    def validate(self, data):
        if not data:
            messagebox.showerror("Error", "Los campos numéricos deben ser válidos")
            return False
        if not data["nombre_producto"]:
            messagebox.showerror("Error", "El nombre del producto es obligatorio")
            return False
        if data["precio_unitario"] < 0:
            messagebox.showerror("Error", "El precio no puede ser negativo")
            return False
        if data["cantidad_producto"] < 0:
            messagebox.showerror("Error", "La cantidad no puede ser negativa")
            return False
        if data["id_insumos"] <= 0:
            messagebox.showerror("Error", "ID Insumo debe ser positivo")
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
            messagebox.showerror("Error", f"No se pudo crear producto: {e}")
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
            messagebox.showwarning("Aviso", "Selecciona un producto para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar producto: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un producto para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el producto seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar producto: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        keys = ["id_producto", "nombre_producto", "precio_unitario", "cantidad_producto", "id_insumos"]
        values = dict(zip(keys, item))
        for k in ("nombre_producto", "precio_unitario", "cantidad_producto", "id_insumos"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))



# from ui.base_crud import BaseCRUD
# from api.type import get, post

# class ProductosTab(BaseCRUD):
#     endpoint = "/productos"
#     columns = ("ID", "Producto", "Precio", "Cantidad", "Insumo")
#     fields = ("nombre_producto", "precio_unitario", "cantidad_producto", "id_insumos")

#     def __init__(self, notebook):
#         super().__init__(notebook, "Productos")

#     def load(self):
#         self.tree.delete(*self.tree.get_children())
#         for p in get(self.endpoint).json():
#             self.tree.insert("", "end", values=(
#                 p["id_producto"],
#                 p["nombre_producto"],
#                 p["precio_unitario"],
#                 p["cantidad_producto"],
#                 p.get("id_insumos")
#             ))

#     def save(self):
#         data = {
#             "nombre_producto": self.form["nombre_producto"].get(),
#             "precio_unitario": float(self.form["precio_unitario"].get()),
#             "cantidad_producto": int(self.form["cantidad_producto"].get()),
#             "id_insumos": int(self.form["id_insumos"].get())
#         }
#         post(self.endpoint, data)
#         self.clear()
#         self.load()
