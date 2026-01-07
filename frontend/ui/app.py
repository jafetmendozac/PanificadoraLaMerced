import tkinter as tk
from tkinter import ttk

# from ui.reportes import ReportesTab
from ui.insumos import InsumosTab
from ui.empleados import EmpleadosTab
from ui.clientes import ClientesTab
from ui.cargos import CargosTab
# from ui.proveedores import ProveedoresTab
from ui.productos import ProductosTab
from ui.pedidos_cliente import PedidosClienteTab

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Panificadora La Merced")
        self.root.geometry("1100x700")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        ClientesTab(self.notebook) #1
        ProductosTab(self.notebook) #2
        EmpleadosTab(self.notebook)#3
        # ProveedoresTab(self.notebook)#4
        # ReportesTab(self.notebook)#5
        InsumosTab(self.notebook)#6
        CargosTab(self.notebook)#7
        PedidosClienteTab(self.notebook)     #8

    def run(self):
        self.root.mainloop()






# import tkinter as tk

# class App(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Mi App")
#         tk.Label(self, text="¡Hola!").pack()

#     def run(self):
#         self.root.mainloop()


# Pago
# Detalle_Pedido
# Estado_Pedido
# Produccion



# import tkinter as tk
# from tkinter import ttk

# from ui.clientes import ClientesTab
# from ui.productos import ProductosTab
# from ui.empleados import EmpleadosTab
# from ui.insumos import InsumosTab
# from ui.pedidos_cliente import PedidosClienteTab
# from ui.reportes import ReportesTab

# class App:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Panificadora La Merced")
#         self.root.geometry("1100x700")

#         notebook = ttk.Notebook(self.root)
#         notebook.pack(fill="both", expand=True)

#         ClientesTab(notebook)
#         ProductosTab(notebook)
#         EmpleadosTab(notebook)
#         InsumosTab(notebook)
#         PedidosClienteTab(notebook)
#         ReportesTab(notebook)

#     def run(self):
#         self.root.mainloop()
