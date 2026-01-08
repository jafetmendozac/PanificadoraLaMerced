
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from api.type import get, post, put, delete

class PedidosProveedorTab:
    endpoint = "/pedidos-proveedor"
    columns = ("ID", "Fecha Pedido", "Fecha Entrega", "Cantidad", "Precio", "Insumo", "Proveedor")

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Pedidos Proveedor")

        self.form = {}
        self._build_form()
        self._build_table()
        self.load()

    # Construir formulario
    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = ["Fecha Pedido (YYYY-MM-DD)", "Fecha Entrega (YYYY-MM-DD)", 
                  "Cantidad", "Precio Unitario", "ID Insumo", "ID Proveedor"]
        fields = ["fecha_pedido", "fecha_entrega", "cantidad", "precio_unitario", "id_insumo", "id_proveedor"]

        for i, (label_text, field_name) in enumerate(zip(labels, fields)):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.form[field_name] = entry

        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)  # <-- botón Limpiar

    # Construir tabla
    def _build_table(self):
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        # Doble clic para cargar en formulario
        self.tree.bind("<Double-1>", self.on_double_click)

    # Cargar datos
    def load(self):
        self.tree.delete(*self.tree.get_children())
        res = get(self.endpoint)
        for p in res.json():
            self.tree.insert("", "end", values=(
                p["id_abastecimiento"],
                p["fecha_pedido"],
                p.get("fecha_entrega", ""),
                p["cantidad"],
                p["precio_unitario"],
                p["id_insumo"],
                p["id_proveedor"]
            ))

    # Validación del formulario
    def validate(self, data):
        try:
            cantidad = float(data["cantidad"])
            precio = float(data["precio_unitario"])
        except ValueError:
            messagebox.showerror("Error", "Cantidad y Precio deben ser números válidos")
            return False

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
            return False
        if precio < 0:
            messagebox.showerror("Error", "El precio debe ser mayor o igual a 0")
            return False

        try:
            fecha_pedido = date.fromisoformat(data["fecha_pedido"])
        except ValueError:
            messagebox.showerror("Error", "Fecha de pedido inválida")
            return False

        fecha_entrega = None
        if data.get("fecha_entrega"):
            try:
                fecha_entrega = date.fromisoformat(data["fecha_entrega"])
            except ValueError:
                messagebox.showerror("Error", "Fecha de entrega inválida")
                return False
            if fecha_entrega < fecha_pedido:
                messagebox.showerror("Error", "La fecha de entrega no puede ser menor a la fecha de pedido")
                return False

        return True

    # Guardar nuevo pedido
    def save(self):
        data = {k: v.get().strip() for k, v in self.form.items()}
        if not self.validate(data):
            return
        # Convertir tipos numéricos
        data["cantidad"] = float(data["cantidad"])
        data["precio_unitario"] = float(data["precio_unitario"])
        post(self.endpoint, data)
        self.clear()
        self.load()

    # Eliminar seleccionado
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún pedido seleccionado")
            return
        for item in selected:
            id_ = self.tree.item(item)["values"][0]
            delete(f"{self.endpoint}/{id_}")
        self.clear()
        self.load()

    # Editar seleccionado
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún pedido seleccionado")
            return
        item = selected[0]
        id_ = self.tree.item(item)["values"][0]
        data = {k: v.get().strip() for k, v in self.form.items()}
        if not self.validate(data):
            return
        data["cantidad"] = float(data["cantidad"])
        data["precio_unitario"] = float(data["precio_unitario"])
        put(f"{self.endpoint}/{id_}", data)
        self.clear()
        self.load()

    # Doble clic: cargar en formulario
    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        values = self.tree.item(item)["values"]
        self.form["fecha_pedido"].delete(0, "end")
        self.form["fecha_pedido"].insert(0, values[1])
        self.form["fecha_entrega"].delete(0, "end")
        self.form["fecha_entrega"].insert(0, values[2])
        self.form["cantidad"].delete(0, "end")
        self.form["cantidad"].insert(0, values[3])
        self.form["precio_unitario"].delete(0, "end")
        self.form["precio_unitario"].insert(0, values[4])
        self.form["id_insumo"].delete(0, "end")
        self.form["id_insumo"].insert(0, values[5])
        self.form["id_proveedor"].delete(0, "end")
        self.form["id_proveedor"].insert(0, values[6])

    # Limpiar formulario
    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
