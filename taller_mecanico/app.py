from datos import CrudMecanico, CrudCliente, CrudVehiculo
from modelo import Mecanico, Cliente, Vehiculo
from tkinter import Tk, Button, messagebox, Toplevel, Label, Entry
from tkinter.ttk import Treeview, Combobox

class Aplicacion:
    def __init__(self, root:Tk) -> None:
        self.root = root
        self.root.title('Taller mecánico')
        self.root.geometry('250x400')
        # Boton para ingresar mecanico
        self.ingresar_mecanico_btn = Button(root, text='Ingresar mecánico', command=self.ingresar_mecanico)
        self.ingresar_mecanico_btn.grid(row=0, column=0, padx=20, pady=20)
        # Boton para mostrar mecanicos
        self.mostrar_mecanicos_btn = Button(root, text='Mostrar mecánicos', command=self.mostrar_mecanicos)
        self.mostrar_mecanicos_btn.grid(row=1, column=0, padx=20, pady=20)
        # Boton para ingresar vehiculo
        self.ingresar_vehiculo_btn = Button(root, text='Ingresar vehículo', command=self.ingresar_vehiculo)
        self.ingresar_vehiculo_btn.grid(row=2, column=0, padx=20, pady=20)
        # Boton para mostrar vehiculos
        self.mostrar_vehiculos_btn = Button(root, text='Mostrar vehículos', command=self.mostrar_vehiculos)
        self.mostrar_vehiculos_btn.grid(row=3, column=0, padx=20, pady=20)

    def ingresar_mecanico(self) -> None:
        NuevoMecanicoVnt(self)
    
    def mostrar_mecanicos(self) -> None:
        MostrarMecanicosVnt(self)

    def ingresar_vehiculo(self) -> None:
        NuevoVehiculoVnt(self)

    def mostrar_vehiculos(self) -> None:
        MostrarVehiculosVnt(self)

class MostrarVehiculosVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de Vehículos")
        self.ventana.geometry("850x300")
        # Tabla con datos de vehiculos
        self.vehiculos_tbl = Treeview(self.ventana, columns=("pat", "mar", "mod", "dueño"), show="headings")
        self.vehiculos_tbl.heading("pat", text="Patente")
        self.vehiculos_tbl.heading("mar", text="Marca")
        self.vehiculos_tbl.heading("mod", text="Modelo")
        self.vehiculos_tbl.heading("dueño", text="Dueño")
        self.vehiculos_tbl.grid(row=0, column=0, padx=20, pady=20)
        self.actualizar_vehiculos()

    def actualizar_vehiculos(self) -> None:
        vehiculos = CrudVehiculo().obtener()
        for v in vehiculos:
            self.vehiculos_tbl.insert("", "end", values=(v.patente, v.marca, v.modelo, "{} {}".format(v.dueño.nombre, v.dueño.apellido)))

class NuevoVehiculoVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Nuevo Vehículo")
        self.ventana.geometry("300x300")
        # Campo de ingreso para la patente
        Label(self.ventana, text="Patente").grid(row=0, column=0, padx=10, pady=10)
        self.patente_ety = Entry(self.ventana)
        self.patente_ety.grid(row=0, column=1, padx=10, pady=10)
        # Campo de ingreso para la marca
        Label(self.ventana, text="Marca").grid(row=1, column=0, padx=10, pady=10)
        self.marca_ety = Entry(self.ventana)
        self.marca_ety.grid(row=1, column=1, padx=10, pady=10)
        # Campo de ingreso para el modelo
        Label(self.ventana, text="Modelo").grid(row=2, column=0, padx=10, pady=10)
        self.modelo_ety = Entry(self.ventana)
        self.modelo_ety.grid(row=2, column=1, padx=10, pady=10)
        # Campo de ingreso para el año
        Label(self.ventana, text="Año").grid(row=3, column=0, padx=10, pady=10)
        self.año_ety = Entry(self.ventana)
        self.año_ety.grid(row=3, column=1, padx=10, pady=10)
        # Combobox para el cliente (dueño)
        Label(self.ventana, text="Dueño del vehículo").grid(row=4, column=0, padx=10, pady=10)
        self.dueño_cmb = Combobox(self.ventana, state="readonly")
        self.dueño_cmb.grid(row=4, column=1, padx=10, pady=10)
        self.cargar_clientes()
        # Botón de ingreso
        self.ingresar_btn = Button(self.ventana, text="Ingresar", command=self.ingresar)
        self.ingresar_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

    def cargar_clientes(self):
        clientes = CrudCliente().obtener()
        values = [] # valores de la lista desplegable del Combobox
        for c in clientes:
            values.append("{} {}".format(c.nombre, c.apellido))
        self.dueño_cmb['values'] = values # copiar la lista de valores a la lista interna

    def ingresar(self):
        patente = self.patente_ety.get()
        marca = self.marca_ety.get()
        modelo = self.modelo_ety.get()
        año = int(self.año_ety.get())
        indice = self.dueño_cmb.current()
        item:str = self.dueño_cmb['values'][indice]
        lista_palabras = item.split()
        nombre = lista_palabras[0]
        apellido = lista_palabras[1]
        #nombre, apellido = item.split()
        cliente = CrudCliente().buscar(nombre, apellido)
        nuevo = Vehiculo(patente, marca, modelo, año, cliente)
        CrudVehiculo().ingresar(nuevo)
        messagebox.showinfo("Nuevo vehículo", "Vehículo ingresado exitosamente")
        self.ventana.destroy()

class MostrarMecanicosVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de mecánicos")
        self.ventana.geometry("650x300")
        # Tabla con datos de mecanicos
        self.mecanicos_tbl = Treeview(self.ventana, columns=("nombre", "apellido", "honorario"), show="headings")
        self.mecanicos_tbl.heading("nombre", text="Nombre")
        self.mecanicos_tbl.heading("apellido", text="Apellido")
        self.mecanicos_tbl.heading("honorario", text="Valor de honorario")
        self.mecanicos_tbl.grid(row=0, column=0, padx=20, pady=20)
        self.actualizar_mecanicos()
            
    def actualizar_mecanicos(self) -> None:
        mecanicos = CrudMecanico().obtener()
        for m in mecanicos:
            self.mecanicos_tbl.insert("", "end", values=(m.nombre, m.apellido, m.honorario))

class NuevoMecanicoVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Nuevo mecánico")
        self.ventana.geometry("300x200")
        # Campo de ingreso para el nombre
        Label(self.ventana, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.nombre_ety = Entry(self.ventana)
        self.nombre_ety.grid(row=0, column=1, padx=10, pady=10)
        # Campo de ingreso para el apellido
        Label(self.ventana, text="Apellido").grid(row=1, column=0, padx=10, pady=10)
        self.apellido_ety = Entry(self.ventana)
        self.apellido_ety.grid(row=1, column=1, padx=10, pady=10)
        # Campo de ingreso para el valor honorario
        Label(self.ventana, text="Valor de honorario").grid(row=2, column=0, padx=10, pady=10)
        self.honorario_ety = Entry(self.ventana)
        self.honorario_ety.grid(row=2, column=1, padx=10, pady=10)
        # Botón de ingreso
        self.ingresar_btn = Button(self.ventana, text="Ingresar", command=self.ingresar)
        self.ingresar_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def ingresar(self) -> None:
        try:
            nombre = self.nombre_ety.get()
            apellido = self.apellido_ety.get()
            honorario = int(self.honorario_ety.get())
            nuevo = Mecanico(nombre, apellido, honorario)
            CrudMecanico().insertar(nuevo)
            messagebox.showinfo("Nuevo mecánico", "Ingreso exitoso")
        except:
            messagebox.showerror("Nuevo mecánico", "Error en ingreso")


# Punto de entrada
root = Tk()
app = Aplicacion(root)
root.mainloop()