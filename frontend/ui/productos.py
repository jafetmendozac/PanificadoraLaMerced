from ui.base_crud import BaseCRUD
from api.type import get, post

class ProductosTab(BaseCRUD):
    endpoint = "/productos"
    columns = ("ID", "Producto", "Precio", "Cantidad", "Insumo")
    fields = ("nombre_producto", "precio_unitario", "cantidad_producto", "id_insumos")

    def __init__(self, notebook):
        super().__init__(notebook, "Productos")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        for p in get(self.endpoint).json():
            self.tree.insert("", "end", values=(
                p["id_producto"],
                p["nombre_producto"],
                p["precio_unitario"],
                p["cantidad_producto"],
                p.get("id_insumos")
            ))

    def save(self):
        data = {
            "nombre_producto": self.form["nombre_producto"].get(),
            "precio_unitario": float(self.form["precio_unitario"].get()),
            "cantidad_producto": int(self.form["cantidad_producto"].get()),
            "id_insumos": int(self.form["id_insumos"].get())
        }
        post(self.endpoint, data)
        self.clear()
        self.load()
