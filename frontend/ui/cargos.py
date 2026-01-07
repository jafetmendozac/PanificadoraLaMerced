# from ui.base_crud import BaseCRUD
# from api.type import get, post, put, delete
# from tkinter import messagebox

# class CargosTab(BaseCRUD):
#     endpoint = "/cargos"
#     columns = ("ID", "Cargo")
#     fields = ("cargo",)

#     def __init__(self, notebook):
#         super().__init__(notebook, "Cargos")
#         self.load()
#         # Bind doble clic en Treeview para editar
#         self.tree.bind("<Double-1>", self.on_double_click)

#     # CARGAR DATOS EN EL TREEVIEW
#     def load(self):
#         self.tree.delete(*self.tree.get_children())
#         for c in get(self.endpoint).json():
#             self.tree.insert("", "end", values=(c["id_cargo"], c["cargo"]))

#     # VALIDACIÓN DE FORMULARIO
#     def validate(self, value):
#         if not value.strip():
#             messagebox.showerror("Error", "El campo 'Cargo' no puede estar vacío")
#             return False
#         if len(value.strip()) > 8:
#             messagebox.showerror("Error", "El campo 'Cargo' no puede tener más de 8 caracteres")
#             return False
#         return True

#     # GUARDAR NUEVO CARGO
#     def save(self):
#         value = self.form["cargo"].get()
#         if not self.validate(value):
#             return
#         post(self.endpoint, {"cargo": value})
#         self.clear()
#         self.load()

#     # ELIMINAR CARGO SELECCIONADO
#     def delete_selected(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showwarning("Advertencia", "No hay ningún cargo seleccionado")
#             return
#         for item in selected:
#             id_cargo = self.tree.item(item)["values"][0]
#             delete(f"{self.endpoint}/{id_cargo}")
#         self.load()
#         self.clear()

#     # EDITAR CARGO SELECCIONADO
#     def edit_selected(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showwarning("Advertencia", "No hay ningún cargo seleccionado")
#             return
#         item = selected[0]
#         id_cargo = self.tree.item(item)["values"][0]
#         new_value = self.form["cargo"].get()
#         if not self.validate(new_value):
#             return
#         put(f"{self.endpoint}/{id_cargo}", {"cargo": new_value})
#         self.clear()
#         self.load()

#     # DOBLE CLIC: cargar valor del Treeview en formulario
#     def on_double_click(self, event):
#         selected = self.tree.selection()
#         if not selected:
#             return
#         item = selected[0]
#         cargo_value = self.tree.item(item)["values"][1]
#         self.form["cargo"].delete(0, "end")
#         self.form["cargo"].insert(0, cargo_value)


import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class CargosTab:
    endpoint = "/cargos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Cargos")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Cargo", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_frame, text="Cargo").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(form_frame)
        entry.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        self.form["cargo"] = entry
        form_frame.columnconfigure(1, weight=1)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

    def _build_table(self):
        columns = ("ID", "Cargo")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar cargos: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for c in data:
            self.tree.insert("", "end", values=(c.get("id_cargo"), str(c.get("cargo", ""))))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        return {"cargo": self.form["cargo"].get().strip()}

    def validate(self, data):
        cargo = data.get("cargo", "")
        if not cargo:
            messagebox.showerror("Error", "El campo 'Cargo' no puede estar vacío")
            return False
        if len(cargo) > 8:
            messagebox.showerror("Error", "El campo 'Cargo' no puede tener más de 8 caracteres")
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
            messagebox.showerror("Error", f"No se pudo crear cargo: {e}")
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
            messagebox.showwarning("Aviso", "Selecciona un cargo para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar cargo: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un cargo para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el cargo seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar cargo: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        # id, cargo
        self.form["cargo"].delete(0, "end")
        self.form["cargo"].insert(0, item[1] if len(item) > 1 else "")
