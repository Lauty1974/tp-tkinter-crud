import tkinter as tk
from tkinter import ttk

from crud import CRUD


campos_vehiculos = [
    "patente",
    "marca",
    "modelo",
    "anio"
]

campos_propietarios = [
    "nombre",
    "apellido",
    "dni",
    "telefono"
]


ventana = tk.Tk()
ventana.title("SISTEMA CRUD")
ventana.geometry("750x550")


titulo = tk.Label(
    ventana,
    text="SISTEMA CRUD"
)

titulo.pack(pady=10)


pestanas = ttk.Notebook(ventana)

pestana_vehiculos = tk.Frame(pestanas)
pestana_propietarios = tk.Frame(pestanas)

pestanas.add(
    pestana_vehiculos,
    text="VEHÍCULOS"
)

pestanas.add(
    pestana_propietarios,
    text="PROPIETARIOS"
)

pestanas.pack(
    expand=True,
    fill="both",
    padx=10,
    pady=10
)


CRUD(
    pestana_vehiculos,
    "VEHÍCULOS",
    campos_vehiculos,
    "vehiculos"
)

CRUD(
    pestana_propietarios,
    "PROPIETARIOS",
    campos_propietarios,
    "propietarios"
)


ventana.mainloop()