import sqlite3


class BaseDatos:
    def __init__(self):
        self.conexion = sqlite3.connect("datos.db")
        self.crear_tablas()

    def crear_tablas(self):
        cursor = self.conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patente TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                anio TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS propietarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT NOT NULL,
                telefono TEXT NOT NULL
            )
        """)

        self.conexion.commit()

    def crear(self, tabla, datos):
        cursor = self.conexion.cursor()

        campos = ", ".join(datos.keys())
        valores = ", ".join(["?"] * len(datos))

        consulta = f"""
            INSERT INTO {tabla} ({campos})
            VALUES ({valores})
        """

        cursor.execute(
            consulta,
            tuple(datos.values())
        )

        self.conexion.commit()

        return cursor.lastrowid

    def obtener_todos(self, tabla):
        cursor = self.conexion.cursor()

        cursor.execute(
            f"SELECT * FROM {tabla}"
        )

        return cursor.fetchall()

    def actualizar(self, tabla, id_registro, datos):
        cursor = self.conexion.cursor()

        modificaciones = ", ".join(
            [f"{campo} = ?" for campo in datos.keys()]
        )

        consulta = f"""
            UPDATE {tabla}
            SET {modificaciones}
            WHERE id = ?
        """

        valores = list(datos.values())
        valores.append(id_registro)

        cursor.execute(
            consulta,
            valores
        )

        self.conexion.commit()

    def eliminar(self, tabla, id_registro):
        cursor = self.conexion.cursor()

        cursor.execute(
            f"DELETE FROM {tabla} WHERE id = ?",
            (id_registro,)
        )

        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()