from ui.base_crud import BaseCRUD
from api.type import get, post

class ClientesTab(BaseCRUD):
    endpoint = "/clientes"
    columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Teléfono")
    fields = ("nombre", "apellido_paterno", "apellido_materno", "telefono_celular")

    def __init__(self, notebook):
        super().__init__(notebook, "Clientes")

    def load(self):
        self.tree.delete(*self.tree.get_children())
        res = get(self.endpoint)
        for c in res.json():
            self.tree.insert("", "end", values=(
                c["id_cliente"],
                c["nombre"],
                c["apellido_paterno"],
                c["apellido_materno"],
                c.get("telefono_celular", "")
            ))

    def save(self):
        data = {k: v.get() for k, v in self.form.items()}
        post(self.endpoint, data)
        self.clear()
        self.load()







# from tkinter import ttk
# from ui.base_crud import BaseCRUDTab
# from api.clientes import listar_clientes, crear_cliente, eliminar_cliente

# class ClientesTab(BaseCRUDTab):
#     def __init__(self, notebook):
#         super().__init__(notebook, "Clientes")
#         self.build_ui()
#         self.cargar()

#     def build_ui(self):
#         form = ttk.LabelFrame(self.frame, text="Nuevo Cliente")
#         form.pack(fill="x", padx=10, pady=10)

#         self.nombre = ttk.Entry(form)
#         self.ap_p = ttk.Entry(form)
#         self.ap_m = ttk.Entry(form)

#         ttk.Label(form, text="Nombre").grid(row=0, column=0)
#         self.nombre.grid(row=0, column=1)

#         ttk.Label(form, text="Apellido Paterno").grid(row=0, column=2)
#         self.ap_p.grid(row=0, column=3)

#         ttk.Label(form, text="Apellido Materno").grid(row=1, column=0)
#         self.ap_m.grid(row=1, column=1)

#         ttk.Button(form, text="Guardar", command=self.guardar).grid(row=2, column=0, pady=5)
#         ttk.Button(form, text="Actualizar", command=self.cargar).grid(row=2, column=1)

#         self.tree = ttk.Treeview(
#             self.frame,
#             columns=("id", "nombre", "ap_p", "ap_m"),
#             show="headings"
#         )
#         for col in self.tree["columns"]:
#             self.tree.heading(col, text=col)

#         self.tree.pack(fill="both", expand=True, padx=10, pady=10)

#         ttk.Button(
#             self.frame,
#             text="Eliminar",
#             command=self.eliminar
#         ).pack(pady=5)

#     def cargar(self):
#         resp = listar_clientes()
#         if resp.status_code != 200:
#             self.show_error("No se pudieron cargar clientes")
#             return

#         self.limpiar_tree()
#         for c in resp.json():
#             self.tree.insert("", "end", values=(
#                 c["id_cliente"],
#                 c["nombre"],
#                 c["apellido_paterno"],
#                 c["apellido_materno"]
#             ))

#     def guardar(self):
#         data = {
#             "nombre": self.nombre.get(),
#             "apellido_paterno": self.ap_p.get(),
#             "apellido_materno": self.ap_m.get()
#         }
#         resp = crear_cliente(data)
#         if resp.status_code == 201:
#             self.show_info("Cliente creado")
#             self.cargar()
#         else:
#             self.show_error(resp.text)

#     def eliminar(self):
#         sel = self.tree.selection()
#         if not sel:
#             return

#         id_cliente = self.tree.item(sel[0])["values"][0]
#         if self.confirm("¿Eliminar cliente?"):
#             eliminar_cliente(id_cliente)
#             self.cargar()
