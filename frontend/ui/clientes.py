import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class ClientesTab:
    endpoint = "/clientes"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Clientes")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Cliente", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        fields = [("nombre", "Nombre"), ("apellido_paterno", "Apellido P"), ("apellido_materno", "Apellido M"), ("telefono_celular", "Teléfono")]
        for i, (key, label) in enumerate(fields):
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
        columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Teléfono")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar clientes: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for c in data:
            # usar str() asegura que Tkinter reciba str en Python
            self.tree.insert("", "end", values=(
                c.get("id_cliente"),
                str(c.get("nombre", "")),
                str(c.get("apellido_paterno", "")),
                str(c.get("apellido_materno", "")),
                str(c.get("telefono_celular", ""))
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        # quitar selección en treeview
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        return {k: v.get().strip() for k, v in self.form.items()}

    def validate(self, data):
        # nombres obligatorios
        for field in ("nombre", "apellido_paterno", "apellido_materno"):
            if not data.get(field):
                messagebox.showerror("Error", f"El campo '{field.replace('_',' ').title()}' es obligatorio")
                return False
        # teléfono: vacío o exactamente 9 dígitos numéricos
        tel = data.get("telefono_celular", "")
        if tel:
            if not tel.isdigit() or len(tel) != 9:
                messagebox.showerror("Error", "El teléfono debe contener exactamente 9 dígitos (solo números)")
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
            messagebox.showerror("Error", f"No se pudo crear cliente: {e}")
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
            messagebox.showwarning("Aviso", "Selecciona un cliente para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar cliente: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un cliente para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el cliente seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar cliente: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        # item orden: id, nombre, apellido_paterno, apellido_materno, telefono
        keys = ["id_cliente", "nombre", "apellido_paterno", "apellido_materno", "telefono_celular"]
        values = dict(zip(keys, item))
        # llenar solo campos del formulario
        for k in ("nombre", "apellido_paterno", "apellido_materno", "telefono_celular"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))
