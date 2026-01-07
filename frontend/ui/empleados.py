from ui.base_crud import BaseCRUD
from api.type import get, post

class EmpleadosTab(BaseCRUD):
    endpoint = "/empleados"
    columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Cargo")
    fields = ("nombre", "apellido_paterno", "apellido_materno", "id_cargo")

    def __init__(self, notebook):
        super().__init__(notebook, "Empleados")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        res = get(self.endpoint)
        for e in res.json():
            self.tree.insert("", "end", values=(
                e["id_empleado"],
                e["nombre"],
                e["apellido_paterno"],
                e["apellido_materno"],
                e["id_cargo"]
            ))

    def save(self):
        data = {
            "nombre": self.form["nombre"].get(),
            "apellido_paterno": self.form["apellido_paterno"].get(),
            "apellido_materno": self.form["apellido_materno"].get(),
            "turno": False,
            "id_cargo": int(self.form["id_cargo"].get())
        }
        post(self.endpoint, data)
        self.clear()
        self.load()
