import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class EmpleadosTab:
    endpoint = "/empleados"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Empleados")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Empleado", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [("nombre", "Nombre"), ("apellido_paterno", "Apellido P"), ("apellido_materno", "Apellido M"), ("id_cargo", "Cargo ID")]
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
        columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Cargo ID")
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
            messagebox.showerror("Error", f"No se pudieron cargar empleados: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for e in data:
            self.tree.insert("", "end", values=(
                e.get("id_empleado"),
                str(e.get("nombre", "")),
                str(e.get("apellido_paterno", "")),
                str(e.get("apellido_materno", "")),
                str(e.get("id_cargo", ""))
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        return {k: v.get().strip() for k, v in self.form.items()}

    def validate(self, data):
        for field in ("nombre", "apellido_paterno", "apellido_materno"):
            if not data.get(field):
                messagebox.showerror("Error", f"El campo '{field.replace('_',' ').title()}' es obligatorio")
                return False
        try:
            if int(data.get("id_cargo", 0)) <= 0:
                messagebox.showerror("Error", "ID de cargo debe ser un número positivo")
                return False
        except ValueError:
            messagebox.showerror("Error", "ID de cargo debe ser un número entero")
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
            messagebox.showerror("Error", f"No se pudo crear empleado: {e}")
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
            messagebox.showwarning("Aviso", "Selecciona un empleado para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar empleado: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un empleado para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el empleado seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar empleado: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        keys = ["id_empleado", "nombre", "apellido_paterno", "apellido_materno", "id_cargo"]
        values = dict(zip(keys, item))
        for k in ("nombre", "apellido_paterno", "apellido_materno", "id_cargo"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))



# from ui.base_crud import BaseCRUD
# from api.type import get, post

# class EmpleadosTab(BaseCRUD):
#     endpoint = "/empleados"
#     columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Cargo")
#     fields = ("nombre", "apellido_paterno", "apellido_materno", "id_cargo")

#     def __init__(self, notebook):
#         super().__init__(notebook, "Empleados")

#     def load(self):
#         self.tree.delete(*self.tree.get_children())
#         res = get(self.endpoint)
#         for e in res.json():
#             self.tree.insert("", "end", values=(
#                 e["id_empleado"],
#                 e["nombre"],
#                 e["apellido_paterno"],
#                 e["apellido_materno"],
#                 e["id_cargo"]
#             ))

#     def save(self):
#         data = {
#             "nombre": self.form["nombre"].get(),
#             "apellido_paterno": self.form["apellido_paterno"].get(),
#             "apellido_materno": self.form["apellido_materno"].get(),
#             "turno": False,
#             "id_cargo": int(self.form["id_cargo"].get())
#         }
#         post(self.endpoint, data)
#         self.clear()
#         self.load()
