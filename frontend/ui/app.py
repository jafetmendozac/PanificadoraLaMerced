import tkinter as tk
from tkinter import ttk

# from ui.reportes import ReportesTab
from ui.insumos import InsumosTab
from ui.empleados import EmpleadosTab
from ui.clientes import ClientesTab
from ui.cargos import CargosTab
from ui.proveedores import ProveedoresTab
from ui.productos import ProductosTab
from ui.pedidos_cliente import PedidosClienteTab
from ui.detalle_pedido import DetallePedidoTab
from ui.estado_pedido import EstadosPedidoTab
from ui.pedido_proveedor import PedidosProveedorTab
from ui.produccion import ProduccionTab

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Panificadora La Merced")
        self.root.geometry("1200x700")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        ClientesTab(self.notebook) #1
        ProductosTab(self.notebook) #2
        EmpleadosTab(self.notebook)#3
        ProveedoresTab(self.notebook)#4
        InsumosTab(self.notebook)#5
        CargosTab(self.notebook)#6
        PedidosClienteTab(self.notebook)     #7
        DetallePedidoTab(self.notebook)     #8
        EstadosPedidoTab(self.notebook)     #9
        PedidosProveedorTab(self.notebook)     #10
        ProduccionTab(self.notebook)     #11

        # ReportesTab(self.notebook)#5


    def run(self):
        self.root.mainloop()