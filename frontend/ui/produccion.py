import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from api.type import get, post, put, delete

class ProduccionTab:
    endpoint = "/produccion"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Producción")

        self.form = {}
        self.turno_var = tk.BooleanVar(value=False)

        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Producción", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [
            ("fecha", "Fecha (YYYY-MM-DD)"),
            ("turno", "Turno (mañana/otro)"),
            ("cantidad_producida", "Cantidad Producida"),
            ("id_empleado", "ID Empleado"),
            ("id_pedido", "ID Pedido")
        ]
        # Fecha
        ttk.Label(form_frame, text=labels[0][1]).grid(row=0, column=0, sticky="w")
        entry_fecha = ttk.Entry(form_frame)
        entry_fecha.grid(row=0, column=1, padx=5, pady=3, sticky="ew")
        self.form["fecha"] = entry_fecha

        # Turno (Checkbutton)
        ttk.Label(form_frame, text=labels[1][1]).grid(row=1, column=0, sticky="w")
        chk = ttk.Checkbutton(form_frame, variable=self.turno_var, text="Turno")
        chk.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        # Cantidad Producida
        ttk.Label(form_frame, text=labels[2][1]).grid(row=2, column=0, sticky="w")
        entry_cant = ttk.Entry(form_frame)
        entry_cant.grid(row=2, column=1, padx=5, pady=3, sticky="ew")
        self.form["cantidad_producida"] = entry_cant

        # ID Empleado
        ttk.Label(form_frame, text=labels[3][1]).grid(row=3, column=0, sticky="w")
        entry_emp = ttk.Entry(form_frame)
        entry_emp.grid(row=3, column=1, padx=5, pady=3, sticky="ew")
        self.form["id_empleado"] = entry_emp

        # ID Pedido
        ttk.Label(form_frame, text=labels[4][1]).grid(row=4, column=0, sticky="w")
        entry_ped = ttk.Entry(form_frame)
        entry_ped.grid(row=4, column=1, padx=5, pady=3, sticky="ew")
        self.form["id_pedido"] = entry_ped

        form_frame.columnconfigure(1, weight=1)

    def _build_buttons(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)

    def _build_table(self):
        columns = ("ID", "Fecha", "Turno", "Cantidad", "ID Empleado", "ID Pedido")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    # ----- Load -----
    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar producciones: {e}")
            return

        self.tree.delete(*self.tree.get_children())
        for p in data:
            # Asegurar str para Tkinter
            self.tree.insert("", "end", values=(
                p.get("id_produccion"),
                str(p.get("fecha", "")),
                str(bool(p.get("turno", False))),
                str(p.get("cantidad_producida", "")),
                str(p.get("id_empleado", "")),
                str(p.get("id_pedido", ""))
            ))

    # ----- Helpers -----
    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")
        self.turno_var.set(False)
        for sel in self.tree.selection():
            self.tree.selection_remove(sel)

    def _collect_form(self):
        return {k: v.get().strip() for k, v in self.form.items()}

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"][0]

    # ----- Validación -----
    def validate(self, data):
        # fecha: si vacío usamos hoy
        fecha_raw = data.get("fecha", "")
        if not fecha_raw:
            # permitir vacío y usar fecha de hoy
            fecha = date.today().isoformat()
            data["fecha"] = fecha
        else:
            try:
                # validar formato ISO
                _ = date.fromisoformat(fecha_raw)
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida. Usa formato YYYY-MM-DD")
                return False

        # cantidad_producida
        try:
            cantidad = int(data.get("cantidad_producida", ""))
        except ValueError:
            messagebox.showerror("Error", "Cantidad producida debe ser un número entero")
            return False
        if cantidad <= 0:
            messagebox.showerror("Error", "Cantidad producida debe ser mayor a 0")
            return False

        # id_empleado e id_pedido
        try:
            id_emp = int(data.get("id_empleado", ""))
            id_ped = int(data.get("id_pedido", ""))
        except ValueError:
            messagebox.showerror("Error", "ID Empleado e ID Pedido deben ser números enteros")
            return False
        if id_emp <= 0 or id_ped <= 0:
            messagebox.showerror("Error", "ID Empleado e ID Pedido deben ser positivos")
            return False

        return True

    # ----- Create -----
    def create(self):
        data = self._collect_form()
        # inyectar turno
        data["turno"] = bool(self.turno_var.get())
        if not self.validate(data):
            return

        payload = {
            "fecha": data["fecha"],
            "turno": data["turno"],
            "cantidad_producida": int(data["cantidad_producida"]),
            "id_empleado": int(data["id_empleado"]),
            "id_pedido": int(data["id_pedido"])
        }

        try:
            res = post(self.endpoint, payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear producción: {e}")
            return

        self.clear()
        self.load()

    # ----- Update -----
    def update_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona una producción para actualizar")
            return

        data = self._collect_form()
        data["turno"] = bool(self.turno_var.get())
        if not self.validate(data):
            return

        payload = {
            "fecha": data["fecha"],
            "turno": data["turno"],
            "cantidad_producida": int(data["cantidad_producida"]),
            "id_empleado": int(data["id_empleado"]),
            "id_pedido": int(data["id_pedido"])
        }

        try:
            res = put(f"{self.endpoint}/{id_}", payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar producción: {e}")
            return

        self.clear()
        self.load()

    # ----- Delete -----
    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona una producción para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar la producción seleccionada?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar producción: {e}")
            return
        self.clear()
        self.load()

    # ----- Double click -----
    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])["values"]
        # orden: ID, Fecha, Turno, Cantidad, ID Empleado, ID Pedido
        _, fecha, turno, cantidad, id_emp, id_ped = item
        # llenar formulario
        self.form["fecha"].delete(0, "end")
        self.form["fecha"].insert(0, fecha if fecha is not None else "")
        self.turno_var.set(True if str(turno).lower() in ("true", "1") else False)
        self.form["cantidad_producida"].delete(0, "end")
        self.form["cantidad_producida"].insert(0, cantidad)
        self.form["id_empleado"].delete(0, "end")
        self.form["id_empleado"].insert(0, id_emp)
        self.form["id_pedido"].delete(0, "end")
        self.form["id_pedido"].insert(0, id_ped)
