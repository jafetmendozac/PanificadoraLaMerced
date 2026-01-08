import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete

class InsumosTab:
    endpoint = "/insumos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Insumos")

        self.form = {}
        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Insumo", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [("nombre_insumo", "Nombre"), ("unidad_medida", "Unidad"), ("stock_minimo", "Stock Min"), ("stock_maximo", "Stock Max")]
        for i, (key, label) in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.form[key] = entry

        form_frame.columnconfigure(1, weight=1)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

    def _build_table(self):
        columns = ("ID", "Nombre", "Unidad", "Stock Min", "Stock Max")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar insumos: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for i in data:
            self.tree.insert("", "end", values=(
                i.get("id_insumo"),
                str(i.get("nombre_insumo", "")),
                str(i.get("unidad_medida", "")),
                str(i.get("stock_minimo", "")),
                str(i.get("stock_maximo", ""))
            ))

    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        try:
            return {
                "nombre_insumo": self.form["nombre_insumo"].get().strip(),
                "unidad_medida": self.form["unidad_medida"].get().strip(),
                "stock_minimo": float(self.form["stock_minimo"].get()),
                "stock_maximo": float(self.form["stock_maximo"].get())
            }
        except ValueError:
            return None

    def validate(self, data):
        if not data:
            messagebox.showerror("Error", "Los valores de stock deben ser numéricos")
            return False
        if not data["nombre_insumo"]:
            messagebox.showerror("Error", "El nombre del insumo es obligatorio")
            return False
        if not data["unidad_medida"]:
            messagebox.showerror("Error", "La unidad de medida es obligatoria")
            return False
        if data["stock_minimo"] < 0 or data["stock_maximo"] < 0:
            messagebox.showerror("Error", "Stock mínimo y máximo no pueden ser negativos")
            return False
        if data["stock_minimo"] > data["stock_maximo"]:
            messagebox.showerror("Error", "Stock mínimo no puede ser mayor que el máximo")
            return False
        return True

    def create(self):
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = post(self.endpoint, data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear insumo: {e}")
            return
        self.clear()
        self.load()

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    def update_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un insumo para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return
        try:
            res = put(f"{self.endpoint}/{id_}", data)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar insumo: {e}")
            return
        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un insumo para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el insumo seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar insumo: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        keys = ["id_insumo", "nombre_insumo", "unidad_medida", "stock_minimo", "stock_maximo"]
        values = dict(zip(keys, item))
        for k in ("nombre_insumo", "unidad_medida", "stock_minimo", "stock_maximo"):
            self.form[k].delete(0, "end")
            self.form[k].insert(0, values.get(k, ""))
