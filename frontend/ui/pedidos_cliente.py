import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete
from datetime import date


class PedidosClienteTab:
    endpoint = "/pedidos"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Pedidos Clientes")

        self.form = {}

        # Variables visuales (backend recibe 0/1)
        self.tipo_entrega_var = tk.StringVar(value="0")  # 0 = Recojo
        self.tipo_pedido_var = tk.StringVar(value="0")   # 0 = Normal

        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    # ======================
    # FORMULARIO
    # ======================
    def _build_form(self):
        form = ttk.LabelFrame(self.frame, text="Formulario Pedido", padding=10)
        form.pack(fill="x", padx=10, pady=10)

        fields = [
            ("id_cliente", "ID Cliente"),
            ("cantidad_producto", "Cantidad"),
            ("fecha", "Fecha (YYYY-MM-DD)"),
            ("id_pago", "ID Pago"),
            ("id_estado", "ID Estado"),
        ]

        for i, (key, label) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(form)
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.form[key] = entry

        # Fecha por defecto hoy
        self.form["fecha"].insert(0, date.today().isoformat())

        # Tipo Entrega (0/1)
        ttk.Label(form, text="Tipo Entrega").grid(row=5, column=0, sticky="w")
        ttk.Combobox(
            form,
            textvariable=self.tipo_entrega_var,
            values=["0", "1"],  # 0 = Recojo, 1 = Delivery
            state="readonly",
            width=17
        ).grid(row=5, column=1, sticky="w")

        # Tipo Pedido (0/1)
        ttk.Label(form, text="Tipo Pedido").grid(row=6, column=0, sticky="w")
        ttk.Combobox(
            form,
            textvariable=self.tipo_pedido_var,
            values=["0", "1"],  # 0 = Normal, 1 = Especial
            state="readonly",
            width=17
        ).grid(row=6, column=1, sticky="w")

        form.columnconfigure(1, weight=1)

    # ======================
    # BOTONES
    # ======================
    def _build_buttons(self):
        frame = ttk.Frame(self.frame)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

    # ======================
    # TABLA
    # ======================
    def _build_table(self):
        cols = ("ID", "Id Cliente", "Fecha", "Cantidad", "Tipo Pedido", "Tipo Entrega", "Id Pago", "Id Estado")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    # ======================
    # LOAD
    # ======================
    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", e)
            return

        self.tree.delete(*self.tree.get_children())

        for p in data:
            self.tree.insert("", "end", values=(
                p["id_pedido"],
                p["id_cliente"],
                p["fecha"],
                p["cantidad_producto"],
                p["tipo_pedido"],
                p["tipo_entrega"],
                p["id_pago"],
                p["id_estado"]
            ))

    # ======================
    # CLEAR
    # ======================
    def clear(self):
        for e in self.form.values():
            e.delete(0, "end")

        self.form["fecha"].insert(0, date.today().isoformat())
        self.tipo_entrega_var.set("0")
        self.tipo_pedido_var.set("0")
        self.tree.selection_remove(*self.tree.selection())

    # ======================
    # FORM DATA
    # ======================
    def _collect_form(self):
        try:
            return {
                "id_cliente": int(self.form["id_cliente"].get()),
                "cantidad_producto": int(self.form["cantidad_producto"].get()),
                "fecha": self.form["fecha"].get(),
                "tipo_entrega": int(self.tipo_entrega_var.get()),
                "tipo_pedido": int(self.tipo_pedido_var.get()),
                "id_pago": int(self.form["id_pago"].get()),
                "id_estado": int(self.form["id_estado"].get()),
            }
        except ValueError:
            return None

    # ======================
    # VALIDATE
    # ======================
    def validate(self, d):
        if not d:
            messagebox.showerror("Error", "Datos inválidos")
            return False
        if d["cantidad_producto"] <= 0:
            messagebox.showerror("Error", "Cantidad inválida")
            return False
        return True

    # ======================
    # CRUD
    # ======================
    def create(self):
        d = self._collect_form()
        if not self.validate(d):
            return
        post(self.endpoint, d)
        self.clear()
        self.load()

    def update_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        id_ = self.tree.item(sel[0])["values"][0]
        d = self._collect_form()
        if not self.validate(d):
            return
        put(f"{self.endpoint}/{id_}", d)
        self.clear()
        self.load()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        id_ = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar pedido?"):
            delete(f"{self.endpoint}/{id_}")
            self.clear()
            self.load()

    # ======================
    # DOUBLE CLICK
    # ======================
    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])["values"]

        keys = ["id_cliente", "fecha", "cantidad_producto", None, None, None, "id_pago", "id_estado"]
        for k, val in zip(keys, v[1:]):
            if k:
                self.form[k].delete(0, "end")
                self.form[k].insert(0, val)

        self.tipo_pedido_var.set(str(v[4]))
        self.tipo_entrega_var.set(str(v[5]))
