import tkinter as tk
from tkinter import ttk
from api.type import get


class ReportesTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="📊 Reportes")

        botones = ttk.Frame(self.frame)
        botones.pack(fill="x", pady=10)

        ttk.Button(botones, text="Ventas por día", command=self.ventas_por_dia).pack(side="left", padx=5)
        # ttk.Button(botones, text="Productos más vendidos", command=self.productos_mas_vendidos).pack(side="left", padx=5)
        ttk.Button(botones, text="Insumos más comprados", command=self.insumos_mas_comprados).pack(side="left", padx=5)
        ttk.Button(botones, text="Clientes frecuentes", command=self.clientes_frecuentes).pack(side="left", padx=5)
        ttk.Button(botones, text="Producción por turno", command=self.produccion_por_turno).pack(side="left", padx=5)
        # ttk.Button(botones, text="Insumos bajo stock", command=self.insumos_bajo_stock).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    # ---------------- UTIL ----------------
    def cargar_tabla(self, columnas, filas):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columnas
        self.tree["show"] = "headings"

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=160)

        for fila in filas:
            self.tree.insert(
                "",
                "end",
                values=[fila[col] for col in columnas]
            )

    # ---------------- REPORTES ----------------
    def ventas_por_dia(self):
        res = get("/reportes/ventas-por-dia").json()
        self.cargar_tabla(["fecha", "total_vendido"], res)

    # def productos_mas_vendidos(self):
    #     res = get("/reportes/productos-mas-vendidos").json()
    #     self.cargar_tabla(["nombre_producto", "total_vendido"], res)

    def insumos_mas_comprados(self):
        res = get("/reportes/insumos-mas-comprados").json()
        self.cargar_tabla(["nombre_insumo", "cantidad_total"], res)

    def clientes_frecuentes(self):
        res = get("/reportes/clientes-frecuentes").json()
        self.cargar_tabla(["nombre", "apellido_paterno", "total_pedidos"], res)

    def produccion_por_turno(self):
        res = get("/reportes/produccion-por-turno").json()

        for r in res:
            r["turno"] = "Mañana" if not r["turno"] else "Tarde"

        self.cargar_tabla(["turno", "total_producido"], res)

    # def insumos_bajo_stock(self):
    #     res = get("/reportes/insumos-bajo-stock").json()
    #     self.cargar_tabla(["nombre_insumo", "stock_minimo", "stock_maximo"], res)
