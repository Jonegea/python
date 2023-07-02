import tkinter as tk
from tkinter import ttk
import sqlite3

class GestionClientesApp(tk.Tk):   #Genera una herencia. creo la clase con sus funciones.
    def __init__(self):#constructor de la clase
        super().__init__()
        self.title("Gestión de Clientes")
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10)

        self.solapa_alta = AltaCliente(self.notebook)
        self.notebook.add(self.solapa_alta, text="Dar de Alta")

        self.solapa_baja = BajaCliente(self.notebook)
        self.notebook.add(self.solapa_baja, text="Dar de Baja")

        self.solapa_buscar = BuscarCliente(self.notebook)
        self.notebook.add(self.solapa_buscar, text="Buscar Cliente")

        self.solapa_listar = ListarClientes(self.notebook)
        self.notebook.add(self.solapa_listar, text="Listar Clientes")

        self.solapa_modificar = ModificarCliente(self.notebook)
        self.notebook.add(self.solapa_modificar, text="Modificar cliente")

        self.crear_tabla()

    def crear_tabla(self):
        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS clientes (codigo INTEGER PRIMARY KEY AUTOINCREMENT not null, nombre TEXT not null, direccion TEXT not null, telefono TEXT not null)")
        c.execute("INSERT INTO sqlite_sequence (name, seq) VALUES ('clientes', 99)")
        conn.commit()
        conn.close()


class AltaCliente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)#llama al constructor padre
        self.label_nombre = tk.Label(self, text="Nombre:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        self.label_direccion = tk.Label(self, text="Dirección:")
        self.label_direccion.pack()
        self.entry_direccion = tk.Entry(self)
        self.entry_direccion.pack()

        self.label_telefono = tk.Label(self, text="Teléfono:")
        self.label_telefono.pack()
        self.entry_telefono = tk.Entry(self)
        self.entry_telefono.pack()

        self.button_alta = tk.Button(self, text="Dar de Alta", command=self.dar_de_alta)
        self.button_alta.pack()

    def dar_de_alta(self):
        nombre = self.entry_nombre.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()

        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("INSERT INTO clientes (nombre, direccion, telefono) VALUES (?, ?, ?)", (nombre, direccion, telefono))
        conn.commit()
        conn.close()
        

        self.entry_nombre.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)


class BajaCliente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label_codigo = tk.Label(self, text="Código:")
        self.label_codigo.pack()
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        self.button_baja = tk.Button(self, text="Dar de Baja", command=self.dar_de_baja)
        self.button_baja.pack()

    def dar_de_baja(self):
        codigo = self.entry_codigo.get()

        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("DELETE FROM clientes WHERE codigo=?", (codigo,))
        conn.commit()
        conn.close()

        self.entry_codigo.delete(0, tk.END)


class BuscarCliente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label_codigo = tk.Label(self, text="Código:")
        self.label_codigo.pack()
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        self.button_buscar = tk.Button(self, text="Buscar Cliente", command=self.buscar_cliente)
        self.button_buscar.pack()

        self.label_resultado = tk.Label(self)
        self.label_resultado.pack()

    def buscar_cliente(self):
        codigo = self.entry_codigo.get()

        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("SELECT * FROM clientes WHERE codigo=?", (codigo,))
        cliente = c.fetchone()
        conn.close()

        if cliente:
            self.label_resultado.config(text=cliente)
        else:
            self.label_resultado.config(text="Cliente no encontrado")


class ListarClientes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.button_listar = tk.Button(self, text="Listar Clientes", command=self.listar_clientes)
        self.button_listar.pack()

        self.label_resultado = tk.Label(self)
        self.label_resultado.pack()

    def listar_clientes(self):
        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("SELECT * FROM clientes")
        clientes = c.fetchall()
        conn.close()

        resultado = ""
        for cliente in clientes:
            resultado += f"Código: {cliente[0]}, Nombre: {cliente[1]}, Dirección: {cliente[2]}, Teléfono: {cliente[3]}\n"
        self.label_resultado.config(text=resultado)


class ModificarCliente(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)#llama al constructor padre
        self.label_codigo = tk.Label(self, text="codigo:")
        self.label_codigo.pack()
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        self.label_nombre = tk.Label(self, text="Nombre:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        self.label_direccion = tk.Label(self, text="Dirección:")
        self.label_direccion.pack()
        self.entry_direccion = tk.Entry(self)
        self.entry_direccion.pack()

        self.label_telefono = tk.Label(self, text="Teléfono:")
        self.label_telefono.pack()
        self.entry_telefono = tk.Entry(self)
        self.entry_telefono.pack()

        self.button_alta = tk.Button(self, text="Modificar Cliente", command=self.modificar_clientes)
        self.button_alta.pack()


    def modificar_clientes(self):
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        conn = sqlite3.connect("clientes.db")
        c = conn.cursor()
        c.execute("UPDATE clientes SET nombre = ?, direccion = ?, telefono = ? WHERE codigo = ?",(nombre, direccion,telefono,codigo))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    app = GestionClientesApp()
    app.mainloop()
