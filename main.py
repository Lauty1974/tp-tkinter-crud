import tkinter as tk
from crud import CRUD


campos_vehiculos = [
    "Patente",
    "Marca",
    "Modelo",
    "Año"
]

campos_propietarios = [
    "Nombre",
    "Apellido",
    "DNI",
    "Teléfono"
]


def abrir_vehiculos():
    vehiculos = CRUD(
        "Vehículos",
        campos_vehiculos
    )
    vehiculos.ejecutar()


def abrir_propietarios():
    propietarios = CRUD(
        "Propietarios",
        campos_propietarios
    )
    propietarios.ejecutar()


ventana = tk.Tk()
ventana.title("Sistema CRUD")
ventana.geometry("300x200")


titulo = tk.Label(
    ventana,
    text="SISTEMA CRUD"
)

titulo.pack(pady=20)


boton_vehiculos = tk.Button(
    ventana,
    text="Vehículos",
    command=abrir_vehiculos
)

boton_vehiculos.pack(pady=5)


boton_propietarios = tk.Button(
    ventana,
    text="Propietarios",
    command=abrir_propietarios
)

boton_propietarios.pack(pady=5)


ventana.mainloop()