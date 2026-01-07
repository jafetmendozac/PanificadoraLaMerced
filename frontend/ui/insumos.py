from ui.base_crud import BaseCRUD
from api.type import get, post

class InsumosTab(BaseCRUD):
    endpoint = "/insumos"
    columns = ("ID", "Nombre", "Unidad", "Min", "Max")
    fields = ("nombre_insumo", "unidad_medida", "stock_minimo", "stock_maximo")

    def __init__(self, notebook):
        super().__init__(notebook, "Insumos")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        for i in get(self.endpoint).json():
            self.tree.insert("", "end", values=(
                i["id_insumo"],
                i["nombre_insumo"],
                i["unidad_medida"],
                i["stock_minimo"],
                i["stock_maximo"]
            ))

    def save(self):
        data = {
            "nombre_insumo": self.form["nombre_insumo"].get(),
            "unidad_medida": self.form["unidad_medida"].get(),
            "stock_minimo": float(self.form["stock_minimo"].get()),
            "stock_maximo": float(self.form["stock_maximo"].get())
        }
        post(self.endpoint, data)
        self.clear()
        self.load()
