from crud_departamento import crud_departamento
from crud_tiempo import crud_tiempo
from crud_empleado import crud_empleado
from crud_proyecto_empleado import crud_proyecto_empleado
from crud_proyecto import crud_proyecto
from crud_usuario import crud_usuario
from modelo import Empleado, Proyecto, Usuario, Tiempo, Departamento
from datetime import datetime
from tkinter import Tk, Button, messagebox, Toplevel, Label, Entry, Frame
from tkinter.ttk import Treeview, Combobox

class Aplicacion:
    def __init__(self, root:Tk) -> None:
        self.root = root
        self.root.title('Aplicacion de Empleados')
        self.root.geometry('250x400')
        # Boton para Gestion de empleados
        self.gestion_empleados_btn = Button(root, text='Gestion de Empleados', command=self.gestion_empleados)
        self.gestion_empleados_btn.grid(row=0, column=0, padx=20, pady=20)
        # Boton para Gestion de departamentos
        self.gestion_departamentos_btn = Button(root, text='Gestión de Departamentos', command=self.gestion_departamentos)
        self.gestion_departamentos_btn.grid(row=1, column=0, padx=20, pady=20)
        # Boton para Gestion de proyectos
        self.gestion_proyectos_btn = Button(root, text='Gestión de Proyectos', command=self.gestion_proyectos)
        self.gestion_proyectos_btn.grid(row=3, column=0, padx=20, pady=20)
        # Boton para Registro de tiempo
        self.registro_tiempo_btn = Button(root, text='Registro de Tiempo', command=self.registro_tiempo)
        self.registro_tiempo_btn.grid(row=2, column=0, padx=20, pady=20)

    def gestion_empleados(self) -> None:
        GestionarEmpleadorVnt(self)
    
    def gestion_departamentos(self) -> None:
        GestionarDepartamentosVnt(self)
    
    def gestion_proyectos(self) -> None:
        ProyectosVnt(self)

    def registro_tiempo(self) -> None:
        GestionarTiempoVnt(self)

class GestionarEmpleadorVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Empleado")
        self.ventana.geometry("250x400")
        # Boton para Añadir Empleado
        self.añadir_empleados_btn = Button(self.ventana, text= "Añadir Empleado", command=self.añadir_empleado)
        self.añadir_empleados_btn.grid(row=0, column=0, padx=20, pady=20)
        # Boton para Visualizar Empleado
        self.visualizar_empleados_btn = Button(self.ventana, text= "Visualizar Empleado", command=self.visualizar_empleados)
        self.visualizar_empleados_btn.grid(row=1, column=0, padx=20, pady=20)
        # Boton para Modificar Empleado
        self.modificar_empleados_btn = Button(self.ventana, text= "Modificar Empleado", command=self.modificar_empleados)
        self.modificar_empleados_btn.grid(row=2, column=0, padx=20, pady=20)
        # Boton para eliminar Empleado
        self.modificar_empleados_btn = Button(self.ventana, text= "Eliminar Empleado", command=self.eliminar_empleados)
        self.modificar_empleados_btn.grid(row=3, column=0, padx=20, pady=20)
        
    def añadir_empleado(self)-> None:
        AñadirEmpleadosVnt(self.app)
    
    def visualizar_empleados(self) -> None:
        VisualizarEmpleadosVnt(self.app)
        
    def modificar_empleados(self) -> None:
        ModificarEmpleadoVnt(self.app)

    def eliminar_empleados(self) -> None:
        EliminarEmpleadosVnt(self.app)

class AñadirEmpleadosVnt:
    def __init__(self, app:GestionarEmpleadorVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Añadir Empleado")
        self.ventana.geometry("300x300")
        # Campo de ingreso para la nombre
        Label(self.ventana, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.nombre_ety = Entry(self.ventana)
        self.nombre_ety.grid(row=0, column=1, padx=10, pady=10)
        # Campo de ingreso para la direccion
        Label(self.ventana, text="Direccion").grid(row=1, column=0, padx=10, pady=10)
        self.direccion_ety = Entry(self.ventana)
        self.direccion_ety.grid(row=1, column=1, padx=10, pady=10)
        # Campo de ingreso para el telefono
        Label(self.ventana, text="Telefono").grid(row=2, column=0, padx=10, pady=10)
        self.telefono_ety = Entry(self.ventana)
        self.telefono_ety.grid(row=2, column=1, padx=10, pady=10)
        # Campo de ingreso para el correo
        Label(self.ventana, text="Correo").grid(row=3, column=0, padx=10, pady=10)
        self.correo_ety = Entry(self.ventana)
        self.correo_ety.grid(row=3, column=1, padx=10, pady=10)
        # Campo de ingreso para la fecha de contrato
        Label(self.ventana, text="Fecha de contrato").grid(row=4, column=0, padx=10, pady=10)
        self.Fecha_contrato_ety = Entry(self.ventana)
        self.Fecha_contrato_ety.grid(row=4, column=1, padx=10, pady=10)
        # Campo de ingreso para el salario
        Label(self.ventana, text="Salario").grid(row=5, column=0, padx=10, pady=10)
        self.salario_ety = Entry(self.ventana)
        self.salario_ety.grid(row=5, column=1, padx=10, pady=10)
        # Campo de ingreso para el salario
        Label(self.ventana, text="Departamento").grid(row=6, column=0, padx=10, pady=10)
        self.nombre_dept_ety = Entry(self.ventana)
        self.nombre_dept_ety.grid(row=6, column=1, padx=10, pady=10)
        # Botón de ingreso
        self.ingresar_btn = Button(self.ventana, text="Ingresar", command=self.ingresar)
        self.ingresar_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=20)

    def ingresar(self):
        try:
            nombre = self.nombre_ety.get()
            direccion = self.direccion_ety.get()
            telefono = self.telefono_ety.get()
            correo = self.correo_ety.get()
            fecha_contrato = self.Fecha_contrato_ety.get()
            fecha_contrato = datetime.strptime(self.Fecha_contrato_ety.get(), "%Y-%m-%d")
            salario = int(self.salario_ety.get())
            nombre_departamento = self.nombre_dept_ety.get()
            nuevo = Empleado(nombre, direccion, telefono, correo, fecha_contrato, salario, nombre_departamento)
            crud_empleado().insertar(nuevo)
            messagebox.showinfo("Nuevo empleado", "Empleado ingresado exitosamente")
            self.ventana.destroy()
        except ValueError:
            messagebox.showerror("Error de Entrada", "Formato de entrada incorrecto")


class VisualizarEmpleadosVnt:    
    def __init__(self, app:GestionarEmpleadorVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de empleados")
        self.ventana.geometry("850x300")
        # Tabla con datos de empleados
        self.empleado_tbl = Treeview(self.ventana, columns=("id_empleado", "nombre", "direccion", "telefono", "correo", "fecha_contrato", "salario", "id_departamento"), show="headings")
        self.empleado_tbl.heading("id_empleado", text="ID")
        self.empleado_tbl.heading("nombre", text="nombre")
        self.empleado_tbl.heading("direccion", text="direccion")
        self.empleado_tbl.heading("telefono", text="telefono")
        self.empleado_tbl.heading("correo", text="correo")
        self.empleado_tbl.heading("fecha_contrato", text="fecha de contrato")
        self.empleado_tbl.heading("salario", text="salario")
        self.empleado_tbl.heading("id_departamento", text="ID Departamento")
        self.empleado_tbl.grid(row=0, column=0, padx=20, pady=20)
        self.ingresar_empleados()

    def ingresar_empleados(self) -> None:
        empleado = crud_empleado().obtener()
        for e in empleado:
            self.empleado_tbl.insert("", "end", 
            values=(e.nombre, e.direccion, e.telefono, e.correo, e.fecha_contrato, e.salario, e.id_departamento, f" {e.nombre}, {e.direccion}, {e.telefono}, {e.correo}, {e.fecha_contrato}, {e.salario}, {e.id_departamento}"))
            
    def obtener_empleados(self) -> None:
        for item in self.tabla_empleados.get_children():
            self.tabla_empleados.delete(item)
        empleados = crud_empleado().obtener()
        for emp in empleados:
            self.tabla_empleados.insert("", "end", values=(
                emp.id_empleado,
                emp.nombre_empleado,
                emp.direccion_empleado,
                emp.numero_telefono,
                emp.correo_electronico_empleado,
                emp.fecha_inicio_contrato,
                emp.salario_empleado,
                emp.departamentos_id_departamentos
            ))


class ModificarEmpleadoVnt:
    def __init__(self, app: GestionarEmpleadorVnt) -> None:
        # Guardamos la referencia a la aplicación principal
        self.app = app
        self.ventana = Toplevel(self.app.root) 
        self.ventana.title("Modificar Empleado")
        self.ventana.geometry("500x500")        
        # Campo de ingreso para el id_empleado
        Label(self.ventana, text="ID Empleado").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=0, column=1, padx=10, pady=5)
        # Campo de ingreso para la contraseña
        Label(self.ventana, text="Contraseña").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entrada_contraseña = Entry(self.ventana, show="*")
        self.entrada_contraseña.grid(row=2, column=1, padx=10, pady=5)
        # Campo de ingreso para el cargo
        Label(self.ventana, text="Cargo").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entrada_cargo = Entry(self.ventana)
        self.entrada_cargo.grid(row=3, column=1, padx=10, pady=5)
        # Campo de ingreso para la nombre
        Label(self.ventana, text="Nombre").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=4, column=1, padx=10, pady=5)
        # Campo de ingreso para la direccion
        Label(self.ventana, text="Dirección").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entrada_direccion = Entry(self.ventana)
        self.entrada_direccion.grid(row=5, column=1, padx=10, pady=5)
        # Campo de ingreso para el telefono
        Label(self.ventana, text="Teléfono").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entrada_telefono = Entry(self.ventana)
        self.entrada_telefono.grid(row=6, column=1, padx=10, pady=5)
        # Campo de ingreso para el correo
        Label(self.ventana, text="Correo").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.entrada_correo = Entry(self.ventana)
        self.entrada_correo.grid(row=7, column=1, padx=10, pady=5)
        # Campo de ingreso para el salario
        Label(self.ventana, text="Salario").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.entrada_salario = Entry(self.ventana)
        # Campo de ingreso para la fecha de contrato
        self.entrada_salario.grid(row=8, column=1, padx=10, pady=5)
        Label(self.ventana, text="Fecha Inicio").grid(row=9, column=0, sticky="w", padx=10, pady=5)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=9, column=1, padx=10, pady=5)
        # Campo de ingreso para el departamento
        Label(self.ventana, text="Departamento").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=10, column=1, padx=10, pady=5)
        
        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=11, column=1, pady=20, padx=10)
        
        self.obtener_empleados()
        self.obtener_departamentos()

    def obtener_empleados(self):
        crud_empleado = crud_empleado()
        empleados = crud_empleado.obtener_todos()
        if not empleados:
            self.empleados_dict = {"Ninguno": None}
            self.combo_id_empleado['values'] = ["Ninguno"]
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre) : id for id, nombre in empleados}
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())
    
    def obtener_departamentos(self):
        crud_departamento = crud_departamento()
        departamentos = crud_departamento.obtener_departamentos()  
        if not departamentos:
            self.departamentos_dict = {"Ninguno": None}
            self.combo_departamento['values'] = ["Ninguno"]
        else:
            self.departamentos_dict = {nombre: id for id, nombre in departamentos}
            self.combo_departamento['values'] = list(self.departamentos_dict.keys())

    def guardar_cambios(self):
        try:
            empleado_seleccionado = self.combo_id_empleado.get()
            empleado_id = self.empleados_dict.get(empleado_seleccionado)
            if not empleado_id:
                messagebox.showerror("Error", "Selecciona un empleado válido.")
                return
            campos_autentificador = {}
            if self.entrada_contraseña.get().strip():
                campos_autentificador['contraseña'] = self.entrada_contraseña.get().strip()
            campos_empleado = {}
            if self.entrada_cargo.get().strip():
                campos_empleado['cargo_rol'] = self.entrada_cargo.get().strip()
            if self.entrada_nombre.get().strip():
                campos_empleado['nombre_empleado'] = self.entrada_nombre.get().strip()
            if self.entrada_direccion.get().strip():
                campos_empleado['direccion_empleado'] = self.entrada_direccion.get().strip()
            if self.entrada_telefono.get().strip():
                campos_empleado['numero_telefono'] = self.entrada_telefono.get().strip()
            if self.entrada_correo.get().strip():
                campos_empleado['correo_electronico_empleado'] = self.entrada_correo.get().strip()
            if self.entrada_salario.get().strip():
                campos_empleado['salario_empleado'] = int(self.entrada_salario.get().strip())
            if self.entrada_fecha_inicio.get().strip():
                campos_empleado['fecha_inicio_contrato'] = datetime.strptime(self.entrada_fecha_inicio.get().strip(), "%Y-%m-%d")
                nombre_departamento = self.combo_departamento.get().strip()
            if nombre_departamento and nombre_departamento != "Ninguno":
                campos_empleado['departamentos_id_departamentos'] = self.departamentos_dict.get(nombre_departamento)
            
            crud = crud_empleado()
            actualizado_autentificador = crud.actualizar_autentificador(empleado_id, campos_autentificador)
            actualizado_empleado = crud.actualizar_empleado(empleado_id, campos_empleado)
            
            if actualizado_autentificador and actualizado_empleado:
                messagebox.showinfo("Éxito", "Empleado modificado correctamente")
                self.ventana.destroy()  
                self.app.obtener_empleados()  
            else:
                messagebox.showerror("Error", "No se pudo modificar el empleado")
        
        except ValueError as e:
            messagebox.showerror("Error de Entrada", f"Formato de entrada incorrecto: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

class EliminarEmpleadosVnt:
    def __init__(self, app: GestionarEmpleadorVnt) -> None:
        self.app = app  
        self.ventana = Toplevel(self.app.root)  
        self.ventana.title("Eliminar Empleado")
        self.ventana.geometry("400x200")
        Label(self.ventana, text="Seleccione el Empleado a eliminar").grid(row=0, column=0, padx=10, pady=10)
        self.combo_empleado = Combobox(self.ventana, state="readonly")
        self.combo_empleado.grid(row=0, column=1, padx=10, pady=10)
        self.obtener_empleados()
        Button(self.ventana, text="Eliminar Empleado", command=self.eliminar_empleado).grid(row=1, column=1, pady=20, padx=10)

    def obtener_empleados(self):
        empleados = self.app.obtener_empleados() 
        if not empleados:
            self.empleados_dict = {}
            self.combo_empleado['values'] = ["No hay empleados disponibles"]
            self.combo_empleado.set("No hay empleados disponibles")
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre): id for id, nombre in empleados}
            self.combo_empleado['values'] = list(self.empleados_dict.keys())
            self.combo_empleado.set("Seleccione un empleado")

    def eliminar_empleado(self):
        empleado_seleccionado = self.combo_empleado.get()
        empleado_id = self.empleados_dict.get(empleado_seleccionado)
        if not empleado_id:
            messagebox.showerror("Error", "Debe seleccionar un empleado válido para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este empleado?")
        if not confirmacion:
            return
        try:
            crud_empleado = crud_empleado()
            if crud_empleado.eliminar_empleado(empleado_id):
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                self.ventana.destroy()
                self.app.obtener_empleados() 
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado.")
        except ValueError:
            messagebox.showerror("Ocurrió un error")

class GestionarDepartamentosVnt:    
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Departamentos")
        self.ventana.geometry("250x400")
        # Botón para Añadir Departamento
        self.añadir_departamento_btn = Button(self.ventana, text="Añadir Departamento", command=self.añadir_departamento)
        self.añadir_departamento_btn.grid(row=0, column=0, padx=20, pady=20)
        # Boton para Visualizar Departamento
        self.visualizar_departamento_btn = Button(self.ventana, text= "Visualizar Departamento", command=self.visualizar_departamento)
        self.visualizar_departamento_btn.grid(row=1, column=0, padx=20, pady=20)
        # Botón para Modificar Departamento
        self.modificar_departamento_btn = Button(self.ventana, text="Modificar Departamento", command=self.modificar_departamento)
        self.modificar_departamento_btn.grid(row=2, column=0, padx=20, pady=20)
        # Botón para Eliminar Departamento
        self.eliminar_departamento_btn = Button(self.ventana, text="Eliminar Departamento", command=self.eliminar_departamento)
        self.eliminar_departamento_btn.grid(row=3, column=0, padx=20, pady=20)

    def añadir_departamento(self) -> None:
        AñadirDepartamentoVnt(self.app)
    
    def visualizar_departamento(self) -> None:
        VisualizarDepartamentoVnt(self.app) 
    
    def modificar_departamento(self) -> None:
        ModificarDepartamentoVnt(self.app)

    def eliminar_departamento(self) -> None: 
        EliminarDepartamentoVnt(self.app) 


class AñadirDepartamentoVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Añadir Departamento")
        self.ventana.geometry("300x300")
        # Campo de ingreso para la nombre
        Label(self.ventana, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.nombre_ety = Entry(self.ventana)
        self.nombre_ety.grid(row=0, column=1, padx=10, pady=10)
        # Botón de ingreso
        self.ingresar_btn = Button(self.ventana, text="Ingresar", command=self.ingresar)
        self.ingresar_btn.grid(row=5, column=0, columnspan=2, padx=20, pady=20)
    
    def ingresar(self):
        nombre = self.nombre_ety.get()
        nuevo_departamento = Departamento(nombre)
        crud_departamento().ingresar(nuevo_departamento)
        messagebox.showinfo("Nuevo departamento", "Departamento ingresado exitosamente")
        self.ventana.destroy()

class VisualizarDepartamentoVnt:
    def __init__(self, app: Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de Departamentos")
        self.ventana.geometry("850x300")
        # Tabla con datos de empleados
        self.departamento_tbl = Treeview(self.ventana, columns=("nombre"), show="headings")
        self.departamento_tbl.heading("nom", text="Nombre")
        self.departamento_tbl.grid(row=0, column=0, padx=20, pady=20)
        self.actualizar_departamento()

    def actualizar_departamento(self):
        departamentos = crud_departamento().listar()  
        self.departamento_tbl.delete(*self.departamento_tbl.get_children())
        for departamento in departamentos:
            self.departamento_tbl.insert("", "end", values=(departamento.nombre,))

class ModificarDepartamentoVnt:
    def __init__(self, app: Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Modificar Departamento")
        self.ventana.geometry("800x600")
        Label(self.ventana, text="Departamentos").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tree_departamentos = Treeview(self.ventana, columns=("id", "nombre", "gerente"), show="headings")
        self.tree_departamentos.heading("id", text="ID Departamento")
        self.tree_departamentos.heading("nombre", text="Nombre Departamento")
        self.tree_departamentos.heading("gerente", text="Gerente")
        self.tree_departamentos.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.tree_departamentos.bind("<<TreeviewSelect>>", self.mostrar_empleados_asociados)
        Label(self.ventana, text="Empleados Asociados al Departamento").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.tree_empleados = Treeview(self.ventana, columns=("id", "nombre", "salario"), show="headings")
        self.tree_empleados.heading("id", text="ID Empleado")
        self.tree_empleados.heading("nombre", text="Nombre")
        self.tree_empleados.heading("salario", text="Salario")
        self.tree_empleados.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.obtener_departamentos()

    def obtener_departamentos(self):
        crud_departamento = crud_departamento()
        departamentos = crud_departamento.obtener_todos_los_departamentos()
        for item in self.tree_departamentos.get_children():
            self.tree_departamentos.delete(item)
        for departamento in departamentos:
            id_departamento, nombre, gerente = departamento
            gerente = gerente if gerente else "Sin Asignar"
            self.tree_departamentos.insert("", "end", values=(id_departamento, nombre, gerente))

    def mostrar_empleados_asociados(self, event):
        selected_item = self.tree_departamentos.selection()
        if not selected_item:
            return
        departamento_id = self.tree_departamentos.item(selected_item, "values")[0]
        for item in self.tree_empleados.get_children():
            self.tree_empleados.delete(item)
        crud_empleado = crud_departamento()
        empleados = crud_empleado.obtener_empleados_por_departamento(departamento_id)
        for emp in empleados:
            id_empleado, nombre, salario = emp
            self.tree_empleados.insert("", "end", values=(id_empleado, nombre, salario))


class EliminarDepartamentoVnt:
    def __init__(self, app: 'EliminarDepartamentoVnt') -> None:
        self.app = app 
        self.ventana = Toplevel(self.app.ventana)  
        self.ventana.title("Eliminar Departamento")
        self.ventana.geometry("400x200")
        # Etiqueta para seleccionar departamento
        Label(self.ventana, text="Seleccione el Departamento a eliminar").grid(row=0, column=0, padx=10, pady=10)
        # elegir el departamento
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=0, column=1, padx=10, pady=10)
        # Cargar los departamentos
        self.obtener_departamentos()
        # Botón para eliminar el departamento
        Button(self.ventana, text="Eliminar Departamento", command=self.eliminar_departamento).grid(row=1, column=1, pady=20, padx=10)

    def obtener_departamentos(self):
        crud_departamento = crud_departamento()
        departamentos = crud_departamento.obtener_departamentos()
        if not departamentos:
            self.departamentos_dict = {"Ninguno": None}
            self.combo_departamento['values'] = ["Ninguno"]
        else:
            self.departamentos_dict = {nombre: id for id, nombre in departamentos}
            self.combo_departamento['values'] = list(self.departamentos_dict.keys())
            self.combo_departamento.set("Seleccione un departamento")

    def eliminar_departamento(self):
        departamento_seleccionado = self.combo_departamento.get()
        departamento_id = self.departamentos_dict.get(departamento_seleccionado)
        if not departamento_id:
            messagebox.showerror("Error", "Debe seleccionar un departamento válido para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este departamento?")
        if not confirmacion:
            return
        try:
            crud_departamento = crud_departamento()
            if crud_departamento.reasignar_y_eliminar(departamento_id):
                messagebox.showinfo("Éxito", "Departamento eliminado correctamente.")
                self.ventana.destroy()
                self.app.obtener_departamentos()  
                messagebox.showerror("Error", "No se pudo eliminar el departamento.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

class ProyectosVnt:
    def __init__(self, app: Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Gestión de Proyectos")
        self.ventana.geometry("250x400")
        marco_botones = Frame(self.ventana)
        marco_botones.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        self.boton_nuevo_proyecto = Button(marco_botones, text="Nuevo Proyecto", command=self.nuevo_proyecto)
        self.boton_nuevo_proyecto.grid(row=0, column=0, padx=20, pady=20)
        self.boton_modificar_proyecto = Button(marco_botones, text="Modificar Proyecto", command=self.modificar_proyecto)
        self.boton_modificar_proyecto.grid(row=1, column=0, padx=20, pady=20)
        self.boton_eliminar_proyecto = Button(marco_botones, text="Eliminar Proyecto", command=self.eliminar_proyecto)
        self.boton_eliminar_proyecto.grid(row=2, column=0, padx=20, pady=20)
        self.boton_actualizar = Button(self.ventana, text="Actualizar", command=self.obtener_proyectos)
        self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
        self.boton_asignar_empleado = Button(marco_botones, text="Asignar empleado a proyecto", command=self.asignar_empleado)
        self.boton_asignar_empleado.grid(row=4, column=0, padx=20, pady=20)
        columnas = ("id_proyecto", "nombre", "descripcion", "fecha_inicio")
    
    def nuevo_proyecto(self):
        VentanaNuevoProyecto(self)

    def modificar_proyecto(self):
        VentanaModificarProyecto(self)

    def eliminar_proyecto(self):
        VentanaEliminarProyecto(self)
    def asignar_empleado(self):
        VentanaAsignarEmpleado(self)

class VisualizarProyectoVnt:
    def __init__(self, app: Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de Proyectos y Empleados Asociados")
        self.ventana.geometry("850x500")
        columnas_proyectos = ("id_proyecto", "nombre", "descripcion", "fecha_inicio")
        self.tabla_proyectos = Treeview(self.ventana, columns=columnas_proyectos, show="headings")
        self.tabla_proyectos.heading("id_proyecto", text="ID Proyecto")
        self.tabla_proyectos.heading("nombre", text="Nombre")
        self.tabla_proyectos.heading("descripcion", text="Descripción")
        self.tabla_proyectos.heading("fecha_inicio", text="Fecha Inicio")
        self.tabla_proyectos.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.actualizar_proyectos()
        
    def actualizar_proyectos(self):
        try:
            for item in self.tabla_proyectos.get_children():
                self.tabla_proyectos.delete(item)
            crud_proyecto = crud_proyecto()
            proyectos = crud_proyecto.obtener()
            if proyectos:
                for p in proyectos:
                    id_proyecto, nombre_proyecto, descripcion, fecha_inicio = p
                    self.tabla_proyectos.insert("", "end", values=(
                        id_proyecto, nombre_proyecto, descripcion, fecha_inicio
                    ))
        except ValueError:
            messagebox.showerror("Error", "Error al cargar proyectos: {}")


class VentanaNuevoProyecto:
    def __init__(self, app:ProyectosVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Ingreso de nuevo Proyecto")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Nombre Proyecto").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=10)
        Label(self.ventana, text="Descripción").grid(row=1, column=0, padx=10, pady=5)
        self.entrada_descripcion = Entry(self.ventana)
        self.entrada_descripcion.grid(row=1, column=1, padx=10, pady=5)
        Label(self.ventana, text="Fecha Inicio (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=2, column=1, padx=10, pady=10)
        Button(self.ventana, text="Ingresar Proyecto", command=self.guardar_cambios).grid(row=3, column=1, pady=20, padx=10)

    def guardar_cambios(self):
        nombre_proyecto = self.entrada_nombre.get().strip()
        descripcion = self.entrada_descripcion.get().strip()
        fecha_inicio_str = self.entrada_fecha_inicio.get().strip()
        if not (nombre_proyecto or descripcion or fecha_inicio_str):
            messagebox.showerror("Error", "Ningún campo puede estar vacío.")
            return
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d") if fecha_inicio_str else None
        except ValueError:
            messagebox.showerror("Error", "La fecha debe estar en el formato YYYY-MM-DD.")
            return
        try:
            crud_proyectos = crud_proyecto()
            proyecto = Proyecto(nombre_proyecto,descripcion,fecha_inicio)
            if crud_proyectos.insertar(proyecto):
                messagebox.showinfo("Éxito", "Proyecto creado correctamente.")
                self.ventana.destroy()
                self.app.obtener_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo crear el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaModificarProyecto:

    def __init__(self, app:ProyectosVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Modificar Proyecto")
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Proyecto a modificar").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_proyecto = Combobox(self.ventana, state="readonly")
        self.combo_proyecto.grid(row=0, column=1, padx=10, pady=5)
        Label(self.ventana, text="Nuevo Nombre").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=1, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nueva descripción").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entrada_descripcion = Entry(self.ventana)
        self.entrada_descripcion.grid(row=2, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nueva Fecha Inicio").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=3, column=1, padx=10, pady=5)
        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=4, column=1, pady=20, padx=10)
        self.obtener_proyectos()

    def obtener_proyectos(self):
        crud_proyectos = crud_proyecto()
        proyectos = crud_proyectos.obtener()
        if not proyectos:
            self.proyectos_dict = {"Ninguno": None}
            self.combo_proyecto['values'] = ["Ninguno"]
            self.combo_proyecto.set("Ninguno")
        else:
            self.proyectos_dict = {nombre_proyecto: id_proyecto for id_proyecto, nombre_proyecto, *_ in proyectos}
            self.combo_proyecto['values'] = list(self.proyectos_dict.keys())
            self.combo_proyecto.set("Seleccione un proyecto")

    def guardar_cambios(self):
        proyecto_seleccionado = self.combo_proyecto.get()
        proyecto_id = self.proyectos_dict.get(proyecto_seleccionado)
        if not proyecto_id:
            messagebox.showerror("Error", "Debe seleccionar un proyecto válido.")
            return
        nuevo_nombre = self.entrada_nombre.get().strip()
        nueva_descripcion = self.entrada_descripcion.get().strip()
        nueva_fecha_inicio = self.entrada_fecha_inicio.get().strip()
        if not nuevo_nombre and not nueva_descripcion and not nueva_fecha_inicio:
            messagebox.showerror("Error", "Debe modificar al menos un campo.")
            return
        campos_actualizar = []
        valores = []
        if nuevo_nombre:
            campos_actualizar.append("nombre_proyecto = %s")
            valores.append(nuevo_nombre)
        if nueva_descripcion:
            campos_actualizar.append("descripcion_proyecto = %s")
            valores.append(nueva_descripcion)
        if nueva_fecha_inicio:
            try:
                fecha_formateada = datetime.strptime(nueva_fecha_inicio, "%Y-%m-%d")
                campos_actualizar.append("fecha_inicio_proyecto = %s")
                valores.append(fecha_formateada)
            except ValueError:
                messagebox.showerror("Error de Formato", "La fecha debe estar en formato YYYY-MM-DD.")
                return
        valores.append(proyecto_id)
        try:
            crud_proyectos = crud_proyecto()
            query = f"UPDATE proyectos SET {', '.join(campos_actualizar)} WHERE id_proyectos = %s"
            if crud_proyectos.actualizar_campos(query, tuple(valores)):
                messagebox.showinfo("Éxito", "Proyecto modificado correctamente.")
                self.ventana.destroy()
                self.app.obtener_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo modificar el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

class VentanaEliminarProyecto:

    def __init__(self, app: ProyectosVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Eliminar Proyecto")
        self.ventana.geometry("400x200")
        Label(self.ventana, text="Seleccione el Proyecto a eliminar").grid(row=0, column=0, padx=10, pady=10)
        self.combo_proyecto = Combobox(self.ventana, state="readonly")
        self.combo_proyecto.grid(row=0, column=1, padx=10, pady=10)
        self.obtener_proyectos()
        Button(self.ventana, text="Eliminar Proyecto", command=self.eliminar_proyecto).grid(row=1, column=1, pady=20, padx=10)

    def obtener_proyectos(self):
        crud_proyectos = crud_proyecto()
        proyectos = crud_proyectos.obtener()
        if not proyectos:
            self.proyectos_dict = {"Ninguno": None}
            self.combo_proyecto['values'] = ["Ninguno"]
            self.combo_proyecto.set("Ninguno")
        else:
            self.proyectos_dict = {nombre_proyecto: id_proyecto for id_proyecto, nombre_proyecto, *_ in proyectos}
            self.combo_proyecto['values'] = list(self.proyectos_dict.keys())
            self.combo_proyecto.set("Seleccione un proyecto")

    def eliminar_proyecto(self):
        proyecto_seleccionado = self.combo_proyecto.get()
        proyecto_id = self.proyectos_dict.get(proyecto_seleccionado)
        if not proyecto_id:
            messagebox.showerror("Error", "Debe seleccionar un proyecto válido para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este proyecto?")
        if not confirmacion:
            return
        try:
            crud_proyecto = crud_proyecto()
            if crud_proyecto.eliminar(proyecto_id):
                messagebox.showinfo("Éxito", "Proyecto eliminado correctamente.")
                self.ventana.destroy()
                self.app.obtener_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaAsignarEmpleado:
    def __init__(self, app: ProyectosVnt) -> None:
            self.app = app
            self.ventana = Toplevel(self.app.ventana)
            self.ventana.title("Asignar empleado a un proyecto")
            self.ventana.geometry("400x200")    
            Label(self.ventana, text="ID Empleado").grid(row=0, column=0, sticky="w", padx=10, pady=5)
            self.combo_id_empleado = Combobox(self.ventana, state="readonly")
            self.combo_id_empleado.grid(row=0, column=1, padx=10, pady=5)
            Label(self.ventana, text="Proyecto por asignar").grid(row=1, column=0, sticky="w", padx=10, pady=5)
            self.combo_proyecto = Combobox(self.ventana, state="readonly")
            self.combo_proyecto.grid(row=1, column=1, padx=10, pady=5)
            self.boton_actualizar = Button(self.ventana, text="Guardar", command=self.guardar)
            self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
            self.obtener_empleados()
            self.obtener_proyectos()

    def obtener_empleados(self):
        crud_empleado = crud_empleado()
        empleados = crud_empleado.obtener_todos()
        if not empleados:
            self.empleados_dict = {"Ninguno": None}
            self.combo_id_empleado['values'] = ["Ninguno"]
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre): id for id, nombre in empleados}
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())

    def obtener_proyectos(self):
        crud_proyectos = crud_proyecto()
        proyectos = crud_proyectos.obtener()
        if not proyectos:
            self.proyectos_dict = {"Ninguno": None}
            self.combo_proyecto['values'] = ["Ninguno"]
            self.combo_proyecto.set("Ninguno")
        else:
            self.proyectos_dict = {nombre_proyecto: id_proyecto for id_proyecto, nombre_proyecto, *_ in proyectos}
            self.combo_proyecto['values'] = list(self.proyectos_dict.keys())
            self.combo_proyecto.set("Seleccione un proyecto")

    def guardar(self):
        crud_guardar = crud_proyecto_empleado()
        proyecto_seleccionado = self.combo_proyecto.get()
        proyecto_id = self.proyectos_dict.get(proyecto_seleccionado)
        if not proyecto_id:
            messagebox.showerror("Error", "Debe seleccionar un proyecto válido.")
            return 
        empleado_seleccionado = self.combo_id_empleado.get()
        empleado_id = self.empleados_dict.get(empleado_seleccionado)
        if not empleado_id:
            messagebox.showerror("Error", "Selecciona un empleado válido.")
            return 
        try:
            if crud_guardar.asignar_empleado_a_proyecto(proyecto_id, empleado_id):
                messagebox.showinfo("Éxito", "Empleado asignado a proyecto correctamente.")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo asignar el empleado al proyecto.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error al asignar: {}".format(e))

class GestionarTiempoVnt:
    def __init__(self, app:Aplicacion) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Gestionar Tiempo")
        self.ventana.geometry("250x400")   
        # Botón para Añadir Tiempo
        self.añadir_tiempo_btn = Button(self.ventana, text="Añadir Tiempo", command=self.añadir_tiempo)
        self.añadir_tiempo_btn.grid(row=0, column=0, padx=20, pady=20)
        # Botón para Visualizar Tiempo
        self.visualizar_tiempo_btn = Button(self.ventana, text="Visualizar Tiempo", command=self.visualizar_tiempo)
        self.visualizar_tiempo_btn.grid(row=1, column=0, padx=20, pady=20)
        # Botón para Modificar Tiempo
        self.modificar_tiempo_btn = Button(self.ventana, text="Modificar Tiempo", command=self.modificar_tiempo)
        self.modificar_tiempo_btn.grid(row=2, column=0, padx=20, pady=20)
        # Botón para Eliminar Tiempo
        self.eliminar_tiempo_btn = Button(self.ventana, text="Eliminar Tiempo", command=self.eliminar_tiempo)
        self.eliminar_tiempo_btn.grid(row=3, column=0, padx=20, pady=20)

    def añadir_tiempo(self) -> None:
        AñadirTiempotoVnt(self.app)
    
    def visualizar_tiempo(self) -> None:
        VisualizarTiempoVnt(self.app)

    def modificar_tiempo(self) -> None:
        ModificarTiempoVnt(self.app)

    def eliminar_tiempo(self) -> None:
        EliminarTiempoVnt(self.app)

class VisualizarTiempoVnt:
    def __init__(self, app: GestionarTiempoVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Lista de registro de tiempo")
        self.ventana.geometry("1050x300")
        # Tabla con datos de empleados
        self.tiempo_tbl = Treeview(self.ventana, columns=("id_tiempo", "fecha", "horas", "descripcion", "id_empleado"), show="headings")
        self.tiempo_tbl.heading("id_tiempo", text="ID")
        self.tiempo_tbl.heading("fecha", text="Fecha")
        self.tiempo_tbl.heading("horas", text="Horas")
        self.tiempo_tbl.heading("descripcion", text="Descripción")
        self.tiempo_tbl.heading("id_empleado", text="ID Empleado")
        self.tiempo_tbl.grid(row=0, column=0, padx=20, pady=20)
        self.ingresar_tiempo()

    def ingresar_tiempo(self) -> None:
        tiempo = crud_tiempo().obtener()
        for t in tiempo:
            self.tiempo_tbl.insert("", "end", 
            values=(t.id_tiempo, t.fecha, t.horas, t.descripcion, t.id_empleado))

class AñadirTiempotoVnt:
    def __init__(self, app:GestionarTiempoVnt):
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Añadir Registro")
        self.ventana.geometry("300x400")
        # Campo de ingreso para Fecha (ej. DD/MM/AAAA)
        Label(self.ventana, text="Fecha (DD/MM/AAAA)").grid(row=0, column=0, padx=10, pady=10)
        self.fecha_ety = Entry(self.ventana)
        self.fecha_ety.grid(row=0, column=1, padx=10, pady=10)
        # Campo de ingreso para Horas (duración del proyecto en horas)
        Label(self.ventana, text="Horas").grid(row=1, column=0, padx=10, pady=10)
        self.horas_ety = Entry(self.ventana)
        self.horas_ety.grid(row=1, column=1, padx=10, pady=10)
        # Campo de ingreso para Descripción
        Label(self.ventana, text="Descripción").grid(row=2, column=0, padx=10, pady=10)
        self.descripcion_ety = Entry(self.ventana)
        self.descripcion_ety.grid(row=2, column=1, padx=10, pady=10)
        # Campo de ingreso para ID Empleado
        Label(self.ventana, text="ID Empleado").grid(row=3, column=0, padx=10, pady=10)
        self.id_empleado_ety = Entry(self.ventana)
        self.id_empleado_ety.grid(row=3, column=1, padx=10, pady=10)
        # Botón de Ingreso
        self.ingresar_btn = Button(self.ventana, text="Ingresar", command=self.ingresar)
        self.ingresar_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    def ingresar(self):
        fecha_str = self.fecha_ety.get()
        horas_str = self.horas_ety.get()
        descripcion = self.descripcion_ety.get()
        id_empleado_str = self.id_empleado_ety.get()
        try:
            fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        except ValueError:
            print("Error: La fecha debe estar en el formato DD/MM/AAAA.")
            return
        try:
            horas = float(horas_str)
            if horas <= 0:
                raise ValueError("Las horas deben ser un número positivo.")
        except ValueError as e:
            print(f"Error: {e}")
            return
        try:
            id_empleado = int(id_empleado_str)
            if id_empleado <= 0:
                raise ValueError("El ID del empleado debe ser un número entero positivo.")
        except ValueError as e:
            print(f"Error: {e}")
            return
        print(f"Proyecto añadido con éxito: Fecha: {fecha.strftime('%d/%m/%Y')}, "
        f"Horas: {horas} horas, Descripción: '{descripcion}', ID Empleado: {id_empleado}")

        self.fecha_ety.delete(0, 'end')
        self.horas_ety.delete(0, 'end')
        self.descripcion_ety.delete(0, 'end')
        self.id_empleado_ety.delete(0, 'end')


class ModificarTiempoVnt:
    def __init__(self, app:GestionarTiempoVnt) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root) 
        self.ventana.title("Modificar Registro de Tiempo")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="ID Registro de tiempo").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_registro = Combobox(self.ventana, state="readonly")
        self.combo_id_registro.grid(row=0, column=1, padx=10, pady=5)
        self.obtener_registro()
        
    def obtener_registro(self):
        crud_tiempo = crud_tiempo()
        registro = crud_tiempo.mostrar_id_registro()
        if not registro:
            self.registro_dict = {"Ninguno": None}
            self.combo_id_registro["values"] = ["Ninguno"]
        else:
            self.combo_id_registro["values"] = registro

class EliminarTiempoVnt:
    pass

# Inicialización de la aplicación
root = Tk()
app = Aplicacion(root)
root.mainloop()

