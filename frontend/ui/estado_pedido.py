import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class EstadosPedidoTab:
    endpoint = "/estados"
    columns = ("ID", "Descripción")

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Estados de Pedido")

        self.form = {}
        self._build_form()
        self._build_table()
        self.load()

    # Construir formulario
    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Descripción").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(form_frame)
        entry.grid(row=0, column=1, padx=5, pady=3)
        self.form["descripcion_estado"] = entry

        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self.save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.edit_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)

    # Construir tabla
    def _build_table(self):
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        # Doble clic para editar
        self.tree.bind("<Double-1>", self.on_double_click)

    # Cargar datos
    def load(self):
        self.tree.delete(*self.tree.get_children())
        res = get(self.endpoint)
        for e in res.json():
            self.tree.insert("", "end", values=(e["id_estado"], e["descripcion_estado"]))

    # Validar formulario
    def validate(self, value):
        if not value.strip():
            messagebox.showerror("Error", "La descripción no puede estar vacía")
            return False
        if len(value.strip()) > 10:
            messagebox.showerror("Error", "La descripción no puede tener más de 10 caracteres")
            return False
        return True

    # Crear nuevo estado
    def save(self):
        value = self.form["descripcion_estado"].get()
        if not self.validate(value):
            return
        post(self.endpoint, {"descripcion_estado": value.strip()})
        self.clear()
        self.load()

    # Eliminar seleccionado
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún estado seleccionado")
            return
        for item in selected:
            id_estado = self.tree.item(item)["values"][0]
            delete(f"{self.endpoint}/{id_estado}")
        self.clear()
        self.load()

    # Editar seleccionado
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún estado seleccionado")
            return
        item = selected[0]
        id_estado = self.tree.item(item)["values"][0]
        new_value = self.form["descripcion_estado"].get()
        if not self.validate(new_value):
            return
        put(f"{self.endpoint}/{id_estado}", {"descripcion_estado": new_value.strip()})
        self.clear()
        self.load()

    # Doble clic: cargar valor del Treeview en formulario
    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        desc = self.tree.item(item)["values"][1]
        self.form["descripcion_estado"].delete(0, "end")
        self.form["descripcion_estado"].insert(0, desc)

    # Limpiar formulario
    def clear(self):
        self.form["descripcion_estado"].delete(0, "end")
