import tkinter as tk
from tkinter import ttk, messagebox
from api.type import get, post, put, delete
from tkinter import ttk, messagebox, filedialog

class EmpleadosTab:
    endpoint = "/empleados"

    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Empleados")

        self.form = {}
        self.turno_var = tk.BooleanVar(value=False)  # variable para turno

        self._build_form()
        self._build_buttons()
        self._build_table()
        self.load()

    def _build_form(self):
        form_frame = ttk.LabelFrame(self.frame, text="Formulario Empleado", padding=10)
        form_frame.pack(fill="x", padx=10, pady=10)

        labels = [
            ("nombre", "Nombre"),
            ("apellido_paterno", "Apellido P"),
            ("apellido_materno", "Apellido M"),
            ("id_cargo", "Cargo ID")
        ]

        for i, (key, label) in enumerate(labels):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=3, sticky="ew")
            self.form[key] = entry

        # 🔹 TURNO (Checkbutton)
        self.turno_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form_frame,
            text="Turno",
            variable=self.turno_var
        ).grid(row=len(labels), column=1, sticky="w", pady=5)

        form_frame.columnconfigure(1, weight=1)


    def _build_buttons(self):
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(btn_frame, text="Guardar", command=self.create).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Actualizar", command=self.update_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_selected).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Importar", command=self.import_placeholder).pack(side="left", padx=5)
        ttk.Button(
            btn_frame,
            text="Importar",
            command=self.abrir_archivos
        ).pack(side="left", padx=5)

    def _build_table(self):
        columns = ("ID", "Nombre", "Apellido P", "Apellido M", "Turno", "Cargo ID")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_double_click)

    def load(self):
        try:
            res = get(self.endpoint)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar empleados: {e}")
            return

        self.tree.delete(*self.tree.get_children())

        for e in data:
            self.tree.insert("", "end", values=(
                e.get("id_empleado"),
                e.get("nombre", ""),
                e.get("apellido_paterno", ""),
                e.get("apellido_materno", ""),
                "Sí" if e.get("turno") else "No",
                e.get("id_cargo", "")
            ))


    def clear(self):
        for entry in self.form.values():
            entry.delete(0, "end")

        self.turno_var.set(False)

        for sel in self.tree.selection():
            self.tree.selection_remove(sel)


    def _collect_form(self):
        data = {k: v.get().strip() for k, v in self.form.items()}
        data["turno"] = self.turno_var.get()
        return data

    def validate(self, data):
        # campos obligatorios
        for field in ("nombre", "apellido_paterno", "apellido_materno"):
            if not data.get(field):
                messagebox.showerror("Error", f"El campo '{field.replace('_',' ').title()}' es obligatorio")
                return False

        # id_cargo debe ser entero positivo
        try:
            id_cargo = int(data.get("id_cargo", 0))
            if id_cargo <= 0:
                messagebox.showerror("Error", "ID de cargo debe ser un número positivo")
                return False
        except ValueError:
            messagebox.showerror("Error", "ID de cargo debe ser un número entero")
            return False

        return True

    def create(self):
        data = self._collect_form()
        if not self.validate(data):
            return

        payload = {
            "nombre": data["nombre"],
            "apellido_paterno": data["apellido_paterno"],
            "apellido_materno": data["apellido_materno"],
            "turno": bool(self.turno_var.get()),   # enviar turno
            "id_cargo": int(data["id_cargo"])
        }

        try:
            res = post(self.endpoint, payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear empleado: {e}")
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
            messagebox.showwarning("Aviso", "Selecciona un empleado para actualizar")
            return
        data = self._collect_form()
        if not self.validate(data):
            return

        payload = {
            "nombre": data["nombre"],
            "apellido_paterno": data["apellido_paterno"],
            "apellido_materno": data["apellido_materno"],
            "turno": bool(self.turno_var.get()),   # enviar turno
            "id_cargo": int(data["id_cargo"])
        }

        try:
            res = put(f"{self.endpoint}/{id_}", payload)
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar empleado: {e}")
            return

        self.clear()
        self.load()

    def delete_selected(self):
        id_ = self.get_selected_id()
        if not id_:
            messagebox.showwarning("Aviso", "Selecciona un empleado para eliminar")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el empleado seleccionado?"):
            return
        try:
            res = delete(f"{self.endpoint}/{id_}")
            res.raise_for_status()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar empleado: {e}")
            return
        self.clear()
        self.load()

    def on_double_click(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        values = self.tree.item(sel[0])["values"]

        self.form["nombre"].delete(0, "end")
        self.form["nombre"].insert(0, values[1])

        self.form["apellido_paterno"].delete(0, "end")
        self.form["apellido_paterno"].insert(0, values[2])

        self.form["apellido_materno"].delete(0, "end")
        self.form["apellido_materno"].insert(0, values[3])

        self.turno_var.set(values[4] == "Sí")

        self.form["id_cargo"].delete(0, "end")
        self.form["id_cargo"].insert(0, values[5])


    def import_placeholder(self):
        # placeholder para botón "Importar" — implementar según necesites
        messagebox.showinfo("Importar", "Funcionalidad de importación no implementada aún.")

    def abrir_archivos(self):
        filedialog.askopenfilename(
            title="Selecciona un archivo",
            initialdir="/",  # raíz del sistema
            filetypes=[("Todos los archivos", "*.*")]
        )