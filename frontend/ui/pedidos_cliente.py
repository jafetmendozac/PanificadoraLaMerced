from ui.base_crud import BaseCRUD
from api.type import get, post
from datetime import date

class PedidosClienteTab(BaseCRUD):
    endpoint = "/pedidos"
    columns = ("ID", "Cliente", "Fecha", "Cantidad", "Estado")
    fields = ("id_cliente", "cantidad_producto")

    def __init__(self, notebook):
        super().__init__(notebook, "Pedidos Clientes")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        for p in get(self.endpoint).json():
            self.tree.insert("", "end", values=(
                p["id_pedido"],
                p["id_cliente"],
                p["fecha"],
                p["cantidad_producto"],
                p["id_estado"]
            ))

    def save(self):
        data = {
            "id_cliente": int(self.form["id_cliente"].get()),
            "cantidad_producto": int(self.form["cantidad_producto"].get()),
            "fecha": date.today().isoformat(),
            "tipo_entrega": False,
            "tipo_pedido": False,
            "id_pago": 1,
            "id_estado": 1
        }
        post(self.endpoint, data)
        self.clear()
        self.load()
