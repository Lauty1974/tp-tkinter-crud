import tkinter as tk
from tkinter import ttk, messagebox


class CRUD:
    def __init__(self, titulo, campos):
        self.titulo = titulo
        self.campos = campos

        self.ventana = tk.Tk()
        self.ventana.title(self.titulo)
        self.ventana.geometry("650x450")

        self.entradas = {}
        self.registros = []
        self.seleccionado = None

        for i, campo in enumerate(self.campos):
            etiqueta = tk.Label(
                self.ventana,
                text=campo
            )
            etiqueta.grid(
                row=i,
                column=0,
                padx=10,
                pady=5
            )

            entrada = tk.Entry(
                self.ventana
            )
            entrada.grid(
                row=i,
                column=1,
                padx=10,
                pady=5
            )

            self.entradas[campo] = entrada

        fila_botones = len(self.campos)

        tk.Button(
            self.ventana,
            text="Crear",
            command=self.crear
        ).grid(
            row=fila_botones,
            column=0,
            padx=5,
            pady=10
        )

        tk.Button(
            self.ventana,
            text="Actualizar",
            command=self.actualizar
        ).grid(
            row=fila_botones,
            column=1,
            padx=5,
            pady=10
        )

        tk.Button(
            self.ventana,
            text="Eliminar",
            command=self.eliminar
        ).grid(
            row=fila_botones,
            column=2,
            padx=5,
            pady=10
        )

        self.tabla = ttk.Treeview(
            self.ventana,
            columns=self.campos,
            show="headings"
        )

        for campo in self.campos:
            self.tabla.heading(
                campo,
                text=campo
            )

            self.tabla.column(
                campo,
                width=120
            )

        self.tabla.grid(
            row=fila_botones + 1,
            column=0,
            columnspan=3,
            padx=10,
            pady=10
        )

        # Detectar selec tabla
        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar
        )

    def crear(self):
        datos = {}

        for campo, entrada in self.entradas.items():
            valor = entrada.get().strip()

            if valor == "":
                messagebox.showwarning(
                    "Campos vacíos",
                    "Complete todos los campos."
                )
                return

            datos[campo] = valor

        self.registros.append(datos)

        self.tabla.insert(
            "",
            tk.END,
            values=list(datos.values())
        )

        self.limpiar()

        messagebox.showinfo(
            "Éxito",
            "Registro creado correctamente."
        )

    def seleccionar(self, evento):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        self.seleccionado = seleccion[0]

        valores = self.tabla.item(
            self.seleccionado,
            "values"
        )

        for campo, valor in zip(self.campos, valores):
            self.entradas[campo].delete(0, tk.END)
            self.entradas[campo].insert(0, valor)

    def actualizar(self):
        if self.seleccionado is None:
            messagebox.showwarning(
                "Sin selección",
                "Seleccione un registro para actualizar."
            )
            return

        datos = {}

        for campo, entrada in self.entradas.items():
            valor = entrada.get().strip()

            if valor == "":
                messagebox.showwarning(
                    "Campos vacíos",
                    "Complete todos los campos."
                )
                return

            datos[campo] = valor

        # Actualizo registros
        indice = self.tabla.index(
            self.seleccionado
        )

        self.registros[indice] = datos

        # Actualizo tabla
        self.tabla.item(
            self.seleccionado,
            values=list(datos.values())
        )

        self.limpiar()

        messagebox.showinfo(
            "Éxito",
            "Registro actualizado correctamente."
        )

    def eliminar(self):
        if self.seleccionado is None:
            messagebox.showwarning(
                "Sin selección",
                "Seleccione un registro para eliminar."
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Está seguro de eliminar el registro?"
        )

        if not respuesta:
            return

        indice = self.tabla.index(
            self.seleccionado
        )

        self.registros.pop(indice)

        self.tabla.delete(
            self.seleccionado
        )

        self.seleccionado = None

        self.limpiar()

        messagebox.showinfo(
            "Éxito",
            "Registro eliminado correctamente."
        )
    def limpiar(self):
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)

        self.seleccionado = None

    def ejecutar(self):
        self.ventana.mainloop()