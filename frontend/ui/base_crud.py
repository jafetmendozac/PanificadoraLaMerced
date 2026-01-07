# import tkinter as tk
# from tkinter import ttk, messagebox
# from api.type import get, post, delete

# class BaseCRUD:
#     endpoint = ""
#     columns = ()
#     fields = ()

#     def __init__(self, notebook, title):
#         self.frame = ttk.Frame(notebook)
#         notebook.add(self.frame, text=title)

#         self.form = {}

#         self._build_form()
#         self._build_table()
#         self.load()

#     def _build_form(self):
#         form_frame = ttk.LabelFrame(self.frame, text="Formulario", padding=10)
#         form_frame.pack(fill="x", padx=10, pady=10)

#         for i, field in enumerate(self.fields):
#             ttk.Label(form_frame, text=field.replace("_", " ").title()).grid(row=i, column=0, sticky="w")
#             entry = ttk.Entry(form_frame)
#             entry.grid(row=i, column=1, padx=5, pady=3)
#             self.form[field] = entry

#         btn_frame = ttk.Frame(form_frame)
#         btn_frame.grid(row=len(self.fields), columnspan=2, pady=10)

#         ttk.Button(btn_frame, text="Guardar", command=self.save).pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="Eliminar", command=self.remove).pack(side="left", padx=5)
#         ttk.Button(btn_frame, text="Actualizar", command=self.load).pack(side="left", padx=5)

#     def _build_table(self):
#         self.tree = ttk.Treeview(self.frame, columns=self.columns, show="headings")
#         self.tree.pack(fill="both", expand=True, padx=10, pady=10)

#         for col in self.columns:
#             self.tree.heading(col, text=col)
#             self.tree.column(col, width=150)

#     def clear(self):
#         for entry in self.form.values():
#             entry.delete(0, "end")

#     def load(self):
#         raise NotImplementedError

#     def save(self):
#         raise NotImplementedError

#     def remove(self):
#         selected = self.tree.selection()
#         if not selected:
#             messagebox.showwarning("Aviso", "Selecciona un registro")
#             return

#         id_ = self.tree.item(selected[0])["values"][0]
#         delete(f"{self.endpoint}/{id_}")
#         self.load()




# import tkinter as tk
# from tkinter import ttk, messagebox

# class BaseCRUDTab:
#     def __init__(self, notebook, title):
#         self.frame = ttk.Frame(notebook)
#         notebook.add(self.frame, text=title)

#         self.tree = None

#     def show_error(self, msg):
#         messagebox.showerror("Error", msg)

#     def show_info(self, msg):
#         messagebox.showinfo("Info", msg)

#     def confirm(self, msg):
#         return messagebox.askyesno("Confirmar", msg)

#     def limpiar_tree(self):
#         for item in self.tree.get_children():
#             self.tree.delete(item)
