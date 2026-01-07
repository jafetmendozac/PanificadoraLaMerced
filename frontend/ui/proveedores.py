from ui.base_crud import BaseCRUD
from api.type import get, post

class ProveedoresTab(BaseCRUD):
    endpoint = "/proveedores"
    columns = ("ID", "Nombre", "Apellido P", "Apellido M", "RUC", "Teléfono")
    fields = ("nombre", "apellido_paterno", "apellido_materno", "ruc", "telefono")

    def __init__(self, notebook):
        super().__init__(notebook, "Proveedores")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        for p in get(self.endpoint).json():
            self.tree.insert("", "end", values=(
                p["id_proveedor"],
                p["nombre"],
                p["apellido_paterno"],
                p["apellido_materno"],
                p["ruc"],
                p.get("telefono", "")
            ))

    def save(self):
        post(self.endpoint, {k: v.get() for k, v in self.form.items()})
        self.clear()
        self.load()
