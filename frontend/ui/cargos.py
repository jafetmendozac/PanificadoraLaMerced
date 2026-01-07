from ui.base_crud import BaseCRUD
from api.type import get, post, put, delete
from tkinter import messagebox

class CargosTab(BaseCRUD):
    endpoint = "/cargos"
    columns = ("ID", "Cargo")
    fields = ("cargo",)

    def __init__(self, notebook):
        super().__init__(notebook, "Cargos")
        self.load()
        # Bind doble clic en Treeview para editar
        self.tree.bind("<Double-1>", self.on_double_click)

    # CARGAR DATOS EN EL TREEVIEW
    def load(self):
        self.tree.delete(*self.tree.get_children())
        for c in get(self.endpoint).json():
            self.tree.insert("", "end", values=(c["id_cargo"], c["cargo"]))

    # VALIDACIÓN DE FORMULARIO
    def validate(self, value):
        if not value.strip():
            messagebox.showerror("Error", "El campo 'Cargo' no puede estar vacío")
            return False
        if len(value.strip()) > 8:
            messagebox.showerror("Error", "El campo 'Cargo' no puede tener más de 8 caracteres")
            return False
        return True

    # GUARDAR NUEVO CARGO
    def save(self):
        value = self.form["cargo"].get()
        if not self.validate(value):
            return
        post(self.endpoint, {"cargo": value})
        self.clear()
        self.load()

    # ELIMINAR CARGO SELECCIONADO
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún cargo seleccionado")
            return
        for item in selected:
            id_cargo = self.tree.item(item)["values"][0]
            delete(f"{self.endpoint}/{id_cargo}")
        self.load()
        self.clear()

    # EDITAR CARGO SELECCIONADO
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No hay ningún cargo seleccionado")
            return
        item = selected[0]
        id_cargo = self.tree.item(item)["values"][0]
        new_value = self.form["cargo"].get()
        if not self.validate(new_value):
            return
        put(f"{self.endpoint}/{id_cargo}", {"cargo": new_value})
        self.clear()
        self.load()

    # DOBLE CLIC: cargar valor del Treeview en formulario
    def on_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        cargo_value = self.tree.item(item)["values"][1]
        self.form["cargo"].delete(0, "end")
        self.form["cargo"].insert(0, cargo_value)
