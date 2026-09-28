import tkinter as tk
from tkinter import ttk, messagebox

from base_datos import BaseDatos


class CRUD:
    def __init__(self, ventana, titulo, campos, tabla_bd):
        self.ventana = ventana
        self.titulo = titulo
        self.campos = campos
        self.tabla_bd = tabla_bd

        self.base_datos = BaseDatos()

        self.entradas = {}
        self.seleccionado = None
        self.id_seleccionado = None

        # Generación dinámica de Labels y Entries
        for i, campo in enumerate(self.campos):
            etiqueta = tk.Label(
                self.ventana,
                text=campo.upper()
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

        # Botones
        fila_botones = len(self.campos)

        tk.Button(
            self.ventana,
            text="CREAR",
            command=self.crear
        ).grid(
            row=fila_botones,
            column=0,
            padx=5,
            pady=10
        )

        tk.Button(
            self.ventana,
            text="ACTUALIZAR",
            command=self.actualizar
        ).grid(
            row=fila_botones,
            column=1,
            padx=5,
            pady=10
        )

        tk.Button(
            self.ventana,
            text="ELIMINAR",
            command=self.eliminar
        ).grid(
            row=fila_botones,
            column=2,
            padx=5,
            pady=10
        )

        # Tabla
        self.tabla = ttk.Treeview(
            self.ventana,
            columns=self.campos,
            show="headings"
        )

        for campo in self.campos:
            self.tabla.heading(
                campo,
                text=campo.upper()
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

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar
        )

        self.cargar_datos()

    # -------------------------
    # CARGAR DATOS
    # -------------------------

    def cargar_datos(self):
        registros = self.base_datos.obtener_todos(
            self.tabla_bd
        )

        for registro in registros:
            id_registro = registro[0]
            valores = registro[1:]

            self.tabla.insert(
                "",
                tk.END,
                iid=str(id_registro),
                values=valores
            )

    # -------------------------
    # CREAR
    # -------------------------

    def crear(self):
        datos = {}

        for campo, entrada in self.entradas.items():
            valor = entrada.get().strip()

            if valor == "":
                messagebox.showwarning(
                    "CAMPOS VACÍOS",
                    "COMPLETE TODOS LOS CAMPOS."
                )
                return

            datos[campo] = valor

        self.base_datos.crear(
            self.tabla_bd,
            datos
        )

        self.limpiar()
        self.recargar_tabla()

        messagebox.showinfo(
            "ÉXITO",
            "REGISTRO CREADO CORRECTAMENTE."
        )

    # -------------------------
    # SELECCIONAR
    # -------------------------

    def seleccionar(self, evento):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        self.seleccionado = seleccion[0]
        self.id_seleccionado = int(
            self.seleccionado
        )

        valores = self.tabla.item(
            self.seleccionado,
            "values"
        )

        for campo, valor in zip(
            self.campos,
            valores
        ):
            self.entradas[campo].delete(
                0,
                tk.END
            )

            self.entradas[campo].insert(
                0,
                valor
            )

    # -------------------------
    # ACTUALIZAR
    # -------------------------

    def actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "SIN SELECCIÓN",
                "SELECCIONE UN REGISTRO PARA ACTUALIZAR."
            )
            return

        datos = {}

        for campo, entrada in self.entradas.items():
            valor = entrada.get().strip()

            if valor == "":
                messagebox.showwarning(
                    "CAMPOS VACÍOS",
                    "COMPLETE TODOS LOS CAMPOS."
                )
                return

            datos[campo] = valor

        self.base_datos.actualizar(
            self.tabla_bd,
            self.id_seleccionado,
            datos
        )

        self.limpiar()
        self.recargar_tabla()

        messagebox.showinfo(
            "ÉXITO",
            "REGISTRO ACTUALIZADO CORRECTAMENTE."
        )

    # -------------------------
    # ELIMINAR
    # -------------------------

    def eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning(
                "SIN SELECCIÓN",
                "SELECCIONE UN REGISTRO PARA ELIMINAR."
            )
            return

        respuesta = messagebox.askyesno(
            "CONFIRMAR",
            "¿ESTÁ SEGURO DE ELIMINAR EL REGISTRO?"
        )

        if not respuesta:
            return

        self.base_datos.eliminar(
            self.tabla_bd,
            self.id_seleccionado
        )

        self.limpiar()
        self.recargar_tabla()

        messagebox.showinfo(
            "ÉXITO",
            "REGISTRO ELIMINADO CORRECTAMENTE."
        )

    # -------------------------
    # RECARGAR TABLA
    # -------------------------

    def recargar_tabla(self):
        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        self.cargar_datos()

    # -------------------------
    # LIMPIAR
    # -------------------------

    def limpiar(self):
        for entrada in self.entradas.values():
            entrada.delete(
                0,
                tk.END
            )

        self.seleccionado = None
        self.id_seleccionado = None