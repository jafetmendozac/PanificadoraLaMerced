import tkinter as tk
from tkinter import ttk
from api.type import get

class ReportesTab:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Reportes")

        ttk.Button(
            self.frame,
            text="Ventas por Día",
            command=self.ventas
        ).pack(pady=10)

        self.output = tk.Text(self.frame, height=25)
        self.output.pack(fill="both", expand=True)

    def ventas(self):
        res = get("/reportes/ventas")
        self.output.delete("1.0", "end")
        self.output.insert("end", res.text)
