from tkinter import Tk, Button, Toplevel, Label, Entry, messagebox, Frame
from tkinter.ttk import Combobox, Treeview
from datetime import datetime
from CRUD_EMPLEADOS import CRUDempleado
from CRUD_DEPARTAMENTOS import CRUDdepartamento
from CRUD_PROYECTOS import CRUDproyecto
from CRUD_REGISTRO_TIEMPO import CRUDRegistroTiempo
from Modelo_Final import Empleado, Proyecto, RegistroTiempo, Usuario
from mysql.connector import MySQLConnection, connect, Error
from API_INDICE import MiIndicador
import hashlib

# Conexion xampp por cmd: c:\xampp\mysql\bin\mysql -u root <

class Clave:
    def cifrar(texto_raw:str) -> str:
        text_codificado = texto_raw.encode('utf-8')
        hash = hashlib.md5(text_codificado).hexdigest()
        return hash

class PantallaLogin:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("EchoTech Soluciones")
        self.root.geometry("400x300")
        self.label_usuario = Label(root, text="Usuario:")
        self.label_usuario.grid(row=0, column=1, padx=10, pady=10)
        self.label_contraseña = Label(root, text="Contraseña:")
        self.label_contraseña.grid(row=1, column=1, padx=10, pady=10)
        self.label_rol = Label(root, text="Rol:")
        self.label_rol.grid(row=2, column=1, padx=10, pady=10)
        self.entry_usuario = Entry(root)
        self.entry_usuario.grid(row=0, column=2, padx=10, pady=10)
        self.entry_contraseña = Entry(root, show="*")
        self.entry_contraseña.grid(row=1, column=2, padx=10, pady=10)
        self.combobox_rol = Combobox(root, state="readonly")
        self.combobox_rol.grid(row=2, column=2, padx=10, pady=10)
        self.boton_iniciar_sesion = Button(root, text="Iniciar sesión",command=self.inicio_usuario)
        self.boton_iniciar_sesion.grid(row=3, column=2, padx=10, pady=10)
        self.boton_registrar_usuario = Button(root, text="Registrar Usuario",command=self.registro_de_usuario)
        self.boton_registrar_usuario.grid(row=4, column=2, padx=10, pady=10)
        self.usuario_logeado = None
        self.cargar_roles()
    
    def cargar_roles(self):
        roles = [
        (1, "Administrador"),
        (0, "Usuario")
        ]
        self.roles_dict = {nombre: id for id, nombre in roles}
        self.combobox_rol['values'] = list(self.roles_dict.keys())
                

    def conectar(self) -> MySQLConnection:
        cnx = connect(user='root', password='', database='ecotechsoluciones')
        return cnx
    
    def inicio_usuario(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        rol = self.combobox_rol.get()
        crud = CRUDempleado()
        if usuario == "" or contraseña == "":
            messagebox.showerror("Error de Campos", "Los campos de entrada de usuario o contraseña están vacíos")
        else:
            resultado = crud.iniciar_sesion(usuario, contraseña, rol)
            if resultado == "admin":
                messagebox.showinfo("Inicio de Sesión", "Inicio de Sesión exitoso como administrador.")
                Programa(self, "admin")
            elif resultado == "usuario":
                messagebox.showinfo("Inicio de Sesión", "Inicio de Sesión exitoso como usuario.")
                Programa(self, "usuario")
            else:
                messagebox.showerror("Error", "El usuario no existe o falló el inicio de sesión.")
    
    def registro_de_usuario(self):
        VentanaRegistroUsuario(self)

class VentanaRegistroUsuario:
    def __init__(self, app: PantallaLogin) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Registro de Usuarios")
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Nombre de Usuario").grid(row=0, column=0, padx=10, pady=10)
        self.entry_usuario = Entry(self.ventana)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)
        Label(self.ventana, text="Contraseña").grid(row=1, column=0, padx=10, pady=10)
        self.entry_contrasenna = Entry(self.ventana, show="*")
        self.entry_contrasenna.grid(row=1, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nombre").grid(row=2, column=0, padx=10, pady=10)
        self.entry_nombre = Entry(self.ventana)
        self.entry_nombre.grid(row=2, column=1, padx=10, pady=10)
        Label(self.ventana, text="Dirección").grid(row=3, column=0, padx=10, pady=10)
        self.entry_direccion = Entry(self.ventana)
        self.entry_direccion.grid(row=3, column=1, padx=10, pady=10)
        Label(self.ventana, text="Telefono").grid(row=4, column=0, padx=10, pady=10)
        self.entry_telefono = Entry(self.ventana)
        self.entry_telefono.grid(row=4, column=1, padx=10, pady=10)
        Label(self.ventana, text="Correo").grid(row=5, column=0, padx=10, pady=10)
        self.entry_correo = Entry(self.ventana)
        self.entry_correo.grid(row=5, column=1, padx=10, pady=10)
        Label(self.ventana, text="Salario").grid(row=6, column=0, padx=10, pady=10)
        self.entry_salario = Entry(self.ventana)
        self.entry_salario.grid(row=6, column=1, padx=10, pady=10)
        Label(self.ventana, text="Fecha Inicio (YYYY-MM-DD)").grid(row=7, column=0, padx=10, pady=10)
        self.entry_fecha_inicio = Entry(self.ventana)
        self.entry_fecha_inicio.grid(row=7, column=1, padx=10, pady=10)
        Label(self.ventana, text="Departamento").grid(row=8, column=0, padx=10, pady=10)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=8, column=1, padx=10, pady=10)
        Button(self.ventana, text="Registrar", command=self.registrar_usuario).grid(row=9, column=1, padx=10, pady=10)
        self.cargar_departamentos()
    
    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
        departamentos = crud_departamento.obtener_departamentos()
        if not departamentos:
            self.departamentos_dict = {"Ninguno": None}
            self.combo_departamento['values'] = ["Ninguno"]
        else:
            self.departamentos_dict = {nombre: id for id, nombre in departamentos}
            self.combo_departamento['values'] = list(self.departamentos_dict.keys())


    def conectar(self) -> MySQLConnection:
        cnx = connect(user='root', password='', database='ecotechsoluciones')
        return cnx
    
    def registrar_usuario(self):
        try:
            usuario = self.entry_usuario.get()
            contraseña = self.entry_contrasenna.get()
            nombre = self.entry_nombre.get()
            direccion = self.entry_direccion.get()
            telefono = self.entry_telefono.get()
            correo = self.entry_correo.get()
            salario = self.entry_salario.get()
            fecha = self.entry_fecha_inicio.get()
            departamento = self.combo_departamento.get()
            id_departamento = self.departamentos_dict.get(departamento)
            hash = Clave.cifrar(contraseña)

            nuevo_empleado = Empleado(
                nombre_usuario=usuario,
                contrasenna=hash,
                es_admin=0,
                nombre_empleado=nombre,
                direccion_empleado=direccion,
                numero_telefono=telefono,
                correo_electronico_empleado=correo,
                salario_empleado=salario,
                fecha_inicio_contrato=fecha,
                departamentos_id_departamentos=id_departamento
            ) 
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql_query = "INSERT INTO usuario (nombre_usuario, contrasenna, es_admin) VALUES (%s, %s, %s);"
            values = (nuevo_empleado.nombre_usuario, nuevo_empleado.contrasenna, nuevo_empleado.es_admin)
            cursor.execute(sql_query, values)
            sql_query2 = """
            INSERT INTO empleados (nombre_empleado, direccion_empleado, numero_telefono, correo_electronico_empleado, 
                                fecha_inicio_contrato, salario_empleado, departamentos_id_departamentos, 
                                usuario_nombre_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            values2 = (nuevo_empleado.nombre_empleado, nuevo_empleado.direccion_empleado, nuevo_empleado.numero_telefono,
                    nuevo_empleado.correo_electronico_empleado, nuevo_empleado.fecha_inicio_contrato, nuevo_empleado.salario_empleado,
                    nuevo_empleado.departamentos_id_departamentos, nuevo_empleado.nombre_usuario)
            cursor.execute(sql_query2, values2)
            cnx.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Usuario", "Usuario Creado con éxito.")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "Hubo un error al crear el usuario.")
        except Exception as e:
            messagebox.showerror("ERROR", "No se pudo registrar el Usuario. Puede que ya se haya registrado.")
            raise Exception("No se pudo registrar un usuario. Error: ", e)
        finally:
            cursor.close()
            cnx.close()
    
    
class Programa:
    def __init__(self, app: PantallaLogin, rol:str) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.root)
        self.ventana.title("Gestión de Empleados")
        self.ventana.geometry("500x300")
        self.boton_gestion_empleado = Button(self.ventana, text="Gestión Empleado", command=self.gestion_empleados)
        self.boton_gestion_empleado.grid(row=1, column=1, padx=10, pady=10)
        self.boton_gestion_departamentos = Button(self.ventana, text="Gestión Departamentos", command=self.gestion_departamentos)
        self.boton_gestion_departamentos.grid(row=2, column=1, padx=10, pady=10)
        self.boton_gestion_proyectos = Button(self.ventana, text="Gestión Proyectos", command=self.gestion_proyectos)
        self.boton_gestion_proyectos.grid(row=3, column=1, padx=10, pady=10)
        self.boton_gestion_registro_tiempo = Button(self.ventana, text="Gestión Registros de Tiempo", command=self.gestion_registro_tiempo)
        self.boton_gestion_registro_tiempo.grid(row=4, column=1, padx=10, pady=10)
        self.boton_consulta_indicadores = Button(self.ventana, text= "Consultar Indicadores", command=self.consultar_indicadores)
        self.boton_consulta_indicadores.grid(row=5, column=1, padx=10, pady=10)

        if rol == "usuario":
            self.esconder_botones_usuario()
            self.boton_gestion_registro_tiempo.config(command=self.gestion_registro_tiempo_usu)
        

    def gestion_empleados(self):
        VentanaGestionEmpleados(self)

    def gestion_departamentos(self):
        VentanaGestionDepartamentos(self)
    
    def gestion_proyectos(self):
        VentanaGestionProyectos(self)

    def gestion_registro_tiempo_usu(self):
        VentanaGestionRegistros(self, "usuario")
        
    def gestion_registro_tiempo(self):
        VentanaGestionRegistros(self, "admin")
        
    def consultar_indicadores(self):
        VentanaConsultaIndicadores(self)
    
    def esconder_botones_usuario(self):
        self.boton_gestion_empleado.grid_forget()
        self.boton_gestion_departamentos.grid_forget()
        self.boton_gestion_proyectos.grid_forget()

class VentanaGestionEmpleados:
    def __init__(self, app: Programa) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Gestión de Empleados")
        self.ventana.geometry("1500x500")
        marco_botones = Frame(self.ventana)
        marco_botones.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        self.boton_nuevo_empleado = Button(marco_botones, text="Nuevo Empleado", command=self.nuevo_empleado)
        self.boton_nuevo_empleado.grid(row=0, column=0, padx=20, pady=20)
        self.boton_modificar_empleado = Button(marco_botones, text="Modificar Empleado", command=self.modificar_empleado)
        self.boton_modificar_empleado.grid(row=0, column=1, padx=20, pady=20)
        self.boton_eliminar_empleado = Button(marco_botones, text="Eliminar Empleado", command=self.eliminar_empleado)
        self.boton_eliminar_empleado.grid(row=0, column=2, padx=20, pady=20)
        self.boton_actualizar = Button(self.ventana, text="Actualizar", command=self.cargar_empleados)
        self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
        
        columnas = ("id_empleado", "usuario", "nombre", "direccion", "telefono", "fecha_inicio", "salario", "departamento")
        self.tabla_empleados = Treeview(self.ventana, columns=columnas, show="headings")
        self.tabla_empleados.heading("id_empleado", text="ID Empleado")
        self.tabla_empleados.heading("usuario", text="Usuario")
        self.tabla_empleados.heading("nombre", text="Nombre")
        self.tabla_empleados.heading("direccion", text="Dirección")
        self.tabla_empleados.heading("telefono", text="Número de Teléfono")
        self.tabla_empleados.heading("fecha_inicio", text="Fecha Inicio Contrato")
        self.tabla_empleados.heading("salario", text="Salario")
        self.tabla_empleados.heading("departamento", text="Departamento")
        self.tabla_empleados.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.cargar_empleados()
    
    def nuevo_empleado(self):
        VentanaNuevoEmpleado(self)
    
    def modificar_empleado(self):
        VentanaModificarEmpleado(self)

    def eliminar_empleado(self):
        VentanaEliminarEmpleado(self)
    
    def cargar_empleados(self) -> None:
        for item in self.tabla_empleados.get_children():
            self.tabla_empleados.delete(item)
        empleados = CRUDempleado().obtener()
        for emp in empleados:
            self.tabla_empleados.insert("", "end", values=(
                emp.id_empleado,
                emp.nombre_usuario,
                emp.nombre_empleado,
                emp.direccion_empleado,
                emp.numero_telefono,
                emp.fecha_inicio_contrato,
                emp.salario_empleado,
                emp.departamentos_id_departamentos
            ))

class VentanaNuevoEmpleado:
    def __init__(self, app: VentanaGestionEmpleados) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Ingreso de nuevo Empleado")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Nombre de Usuario").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_nombre_usuario = Entry(self.ventana)
        self.entrada_nombre_usuario.grid(row=0, column=1, padx=10, pady=10)
        Label(self.ventana, text="Contraseña").grid(row=1, column=0, padx=10, pady=10)
        self.entrada_contrasenna = Entry(self.ventana, show="*")
        self.entrada_contrasenna.grid(row=1, column=1, padx=10, pady=10)
        Label(self.ventana, text="Rol").grid(row=2, column=0, padx=10, pady=10)
        self.combo_entrada_rol = Combobox(self.ventana, state="readonly")
        self.combo_entrada_rol.grid(row=2, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nombre").grid(row=3, column=0, padx=10, pady=10)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=3, column=1, padx=10, pady=10)
        Label(self.ventana, text="Dirección").grid(row=4, column=0, padx=10, pady=10)
        self.entrada_direccion = Entry(self.ventana)
        self.entrada_direccion.grid(row=4, column=1, padx=10, pady=10)
        Label(self.ventana, text="Telefono").grid(row=5, column=0, padx=10, pady=10)
        self.entrada_telefono = Entry(self.ventana)
        self.entrada_telefono.grid(row=5, column=1, padx=10, pady=10)
        Label(self.ventana, text="Correo").grid(row=6, column=0, padx=10, pady=10)
        self.entrada_correo = Entry(self.ventana)
        self.entrada_correo.grid(row=6, column=1, padx=10, pady=10)
        Label(self.ventana, text="Salario").grid(row=7, column=0, padx=10, pady=10)
        self.entrada_salario = Entry(self.ventana)
        self.entrada_salario.grid(row=7, column=1, padx=10, pady=10)
        Label(self.ventana, text="Fecha Inicio (YYYY-MM-DD)").grid(row=8, column=0, padx=10, pady=10)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=8, column=1, padx=10, pady=10)
        Label(self.ventana, text="Departamento").grid(row=9, column=0, padx=10, pady=10)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=9, column=1, padx=10, pady=10)
        Button(self.ventana, text="Ingresar", command=self.ingresar_empleado).grid(row=10, column=1, padx=10, pady=10)
        self.cargar_departamentos()
        self.cargar_roles()
        
    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
        departamentos = crud_departamento.obtener_departamentos()
        if not departamentos:
            self.departamentos_dict = {"Ninguno": None}
            self.combo_departamento['values'] = ["Ninguno"]
        else:
            self.departamentos_dict = {nombre: id for id, nombre in departamentos}
            self.combo_departamento['values'] = list(self.departamentos_dict.keys())
    
    def cargar_roles(self):
        roles = [
        (1, "Administrador"),
        (0, "Usuario")
        ]
        self.roles_dict = {nombre: id for id, nombre in roles}
        self.combo_entrada_rol['values'] = list(self.roles_dict.keys())

    def ingresar_empleado(self):
        try:
            id_usuario = self.entrada_nombre_usuario.get()
            contrasenna = self.entrada_contrasenna.get()
            rol = self.combo_entrada_rol.get()
            rol = self.roles_dict.values()
            nombre = self.entrada_nombre.get()
            direccion = self.entrada_direccion.get()
            telefono = self.entrada_telefono.get()
            correo = self.entrada_correo.get()
            salario = int(self.entrada_salario.get())
            fecha_inicio = datetime.strptime(self.entrada_fecha_inicio.get(), "%Y-%m-%d")
            nombre_departamento = self.combo_departamento.get()
            id_departamento = self.departamentos_dict.get(nombre_departamento)

            hash = Clave.cifrar(contrasenna)
            
            nuevo_empleado = Empleado(
                nombre_usuario=id_usuario,
                contrasenna=hash,
                es_admin=rol,
                nombre_empleado=nombre,
                direccion_empleado=direccion,
                numero_telefono=telefono,
                correo_electronico_empleado=correo,
                salario_empleado=salario,
                fecha_inicio_contrato=fecha_inicio,
                departamentos_id_departamentos=id_departamento
            )
            crud = CRUDempleado()
            if crud.insertar(nuevo_empleado):
                messagebox.showinfo("Éxito", "Empleado ingresado correctamente")
                self.ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo ingresar el empleado")
        except ValueError as e:
            messagebox.showerror("Error de Entrada", "Formato de entrada incorrecto: {}".format(e))
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error inesperado: {}".format(e))

class VentanaModificarEmpleado:
    def __init__(self, app: VentanaGestionEmpleados) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Modificar Empleado")
        self.ventana.geometry("500x500")
        Label(self.ventana, text="ID Empleado").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=0, column=1, padx=10, pady=5)
        Label(self.ventana, text="Contraseña").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entrada_contrasenna = Entry(self.ventana, show="*")
        self.entrada_contrasenna.grid(row=2, column=1, padx=10, pady=5)
        Label(self.ventana, text="Rol").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.combo_entrada_rol = Combobox(self.ventana, state="readonly")
        self.combo_entrada_rol.grid(row=3, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nombre").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=4, column=1, padx=10, pady=5)
        Label(self.ventana, text="Dirección").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entrada_direccion = Entry(self.ventana)
        self.entrada_direccion.grid(row=5, column=1, padx=10, pady=5)
        Label(self.ventana, text="Teléfono").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entrada_telefono = Entry(self.ventana)
        self.entrada_telefono.grid(row=6, column=1, padx=10, pady=5)
        Label(self.ventana, text="Correo").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.entrada_correo = Entry(self.ventana)
        self.entrada_correo.grid(row=7, column=1, padx=10, pady=5)
        Label(self.ventana, text="Salario").grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.entrada_salario = Entry(self.ventana)
        self.entrada_salario.grid(row=8, column=1, padx=10, pady=5)
        Label(self.ventana, text="Fecha Inicio").grid(row=9, column=0, sticky="w", padx=10, pady=5)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=9, column=1, padx=10, pady=5)
        Label(self.ventana, text="Departamento").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=10, column=1, padx=10, pady=5)
        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=11, column=1, pady=20, padx=10)
        self.cargar_empleados()
        self.cargar_departamentos()
        self.cargar_roles()

    def cargar_roles(self):
        roles = [
        (1, "Administrador"),
        (2, "Usuario")
        ]
        self.roles_dict = {nombre: id for id, nombre in roles}
        self.combo_entrada_rol['values'] = list(self.roles_dict.keys())

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        if not empleados:
            self.empleados_dict = {"Ninguno": None}
            self.combo_id_empleado['values'] = ["Ninguno"]
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre): id for id, nombre in empleados}
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())

    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
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
            campos_usuario = {}
            hash = Clave.cifrar(self.entrada_contrasenna.get().strip())
            if self.entrada_contrasenna.get().strip():
                campos_usuario['contrasenna'] = hash
            if self.combo_entrada_rol.get().strip():
                campos_usuario['es_admin'] = self.combo_entrada_rol.get().strip()
            campos_empleado = {}
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
            crud = CRUDempleado()
            actualizado_usuario = crud.actualizar_usuario(empleado_id, campos_usuario)
            actualizado_empleado = crud.actualizar_empleado(empleado_id, campos_empleado)
            if actualizado_usuario and actualizado_empleado:
                messagebox.showinfo("Éxito", "Empleado modificado correctamente")
                self.ventana.destroy()
                self.app.cargar_empleados()
            else:
                messagebox.showerror("Error", "No se pudo modificar el empleado")
        except ValueError as e:
            messagebox.showerror("Error de Entrada", "Formato de entrada incorrecto: {}".format(e))
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error inesperado: {}".format(e))

class VentanaEliminarEmpleado:

    def __init__(self, app: VentanaGestionEmpleados) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Eliminar Empleado")
        self.ventana.geometry("400x200")
        Label(self.ventana, text="Seleccione el Empleado a eliminar").grid(row=0, column=0, padx=10, pady=10)
        self.combo_empleado = Combobox(self.ventana, state="readonly")
        self.combo_empleado.grid(row=0, column=1, padx=10, pady=10)
        self.cargar_empleados()
        Button(self.ventana, text="Eliminar Empleado", command=self.eliminar_empleado).grid(row=1, column=1, pady=20, padx=10)

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
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
            crud_empleado = CRUDempleado()
            if crud_empleado.eliminar_empleado(empleado_id):
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                self.ventana.destroy()
                self.app.cargar_empleados()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el empleado.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaGestionDepartamentos:
    
    def __init__(self, app: Programa) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Gestión de Departamentos")
        self.ventana.geometry("1080x700")
        marco_botones = Frame(self.ventana)
        marco_botones.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        self.boton_nuevo_departamento = Button(marco_botones, text="Nuevo Departamento", command=self.nuevo_departamento)
        self.boton_nuevo_departamento.grid(row=0, column=0, padx=20, pady=20)
        self.boton_modificar_departamento = Button(marco_botones, text="Modificar Departamento / Asignar Gerente", command=self.modificar_departamento)
        self.boton_modificar_departamento.grid(row=0, column=1, padx=20, pady=20)
        self.boton_eliminar_departamento = Button(marco_botones, text="Eliminar Departamento", command=self.eliminar_departamento)
        self.boton_eliminar_departamento.grid(row=0, column=2, padx=20, pady=20)
        self.boton_ver_departamento = Button(marco_botones, text="Ver Departamentos", command=self.ver_departamento)
        self.boton_ver_departamento.grid(row=0, column=3, padx=20, pady=20)
        self.boton_actualizar = Button(self.ventana, text="Actualizar", command=self.cargar_departamentos)
        self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
        columnas = ("id_departamento", "nombre", "Gerente departamento")
        self.tabla_departamento = Treeview(self.ventana, columns=columnas, show="headings")
        self.tabla_departamento.heading("id_departamento", text="ID Departamento")
        self.tabla_departamento.heading("nombre", text="Nombre")
        self.tabla_departamento.heading("Gerente departamento", text="Gerente Departamento")
        self.tabla_departamento.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.cargar_departamentos()

    def cargar_departamentos(self):
        try:
            for item in self.tabla_departamento.get_children():
                self.tabla_departamento.delete(item)
            crud_departamento = CRUDdepartamento()
            departamentos = crud_departamento.mostrar_departamentos_con_gerente()
            if departamentos:
                for departamento in departamentos:
                    id_departamento, nombre_departamento, nombre_gerente = departamento
                    nombre_gerente = nombre_gerente if nombre_gerente else "Sin Asignar"
                    self.tabla_departamento.insert("", "end", values=(
                        id_departamento, nombre_departamento, nombre_gerente
                    ))
        except Error as e:
            messagebox.showerror("Error", "Error al cargar departamentos: {}".format(e))

    def nuevo_departamento(self):
        VentanaNuevoDepartamento(self)

    def modificar_departamento(self):
        VentanaModificarDepartamento(self)

    def eliminar_departamento(self):
        VentanaEliminarDepartamento(self)

    def ver_departamento(self):
        VentanaVerDepartamento(self)

class VentanaNuevoDepartamento:
    def __init__(self, app: VentanaGestionDepartamentos) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Ingreso de nuevo Departamento")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=0, column=1, padx=10, pady=10)
        Label(self.ventana, text="Gerente").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=1, column=1, padx=10, pady=5)
        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=2, column=1, pady=20, padx=10)
        self.cargar_empleados()

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        self.empleados_dict = {"Ninguno": None}
        if empleados:
            self.empleados_dict.update({"{} - {}".format(id, nombre): id for id, nombre in empleados})
        self.combo_id_empleado['values'] = list(self.empleados_dict.keys())
        self.combo_id_empleado.set("Ninguno")

    def guardar_cambios(self):
        nombre_departamento = self.entrada_nombre.get().strip()
        gerente_seleccionado = self.combo_id_empleado.get()
        id_gerente = self.empleados_dict.get(gerente_seleccionado)
        if not nombre_departamento:
            messagebox.showerror("Error", "El nombre del departamento no puede estar vacío.")
            return
        try:
            crud_departamento = CRUDdepartamento()
            if crud_departamento.insertar_departamento(nombre_departamento, id_gerente):
                messagebox.showinfo("Éxito", "Departamento creado correctamente.")
                self.ventana.destroy()
                self.app.cargar_departamentos()
            else:
                messagebox.showerror("Error", "No se pudo crear el departamento.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaModificarDepartamento:

    def __init__(self, app: VentanaGestionDepartamentos) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Modificar Departamento")
        self.ventana.geometry("500x500")
        Label(self.ventana, text="Departamento a modificar").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=0, column=1, padx=10, pady=5)
        Label(self.ventana, text="Nuevo Nombre").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entrada_nombre = Entry(self.ventana)
        self.entrada_nombre.grid(row=1, column=1, padx=10, pady=10)
        Label(self.ventana, text="Nuevo Gerente").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=2, column=1, padx=10, pady=5)
        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=3, column=1, pady=20, padx=10)
        self.cargar_departamentos()
        self.cargar_empleados()

    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
        departamentos = crud_departamento.obtener_departamentos()
        if not departamentos:
            self.departamentos_dict = {"Ninguno": None}
            self.combo_departamento['values'] = ["Ninguno"]
        else:
            self.departamentos_dict = {nombre: id for id, nombre in departamentos}
            self.combo_departamento['values'] = list(self.departamentos_dict.keys())
            self.combo_departamento.set("Seleccione un departamento")

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        self.empleados_dict = {"Ninguno": None}      
        if empleados:
            self.empleados_dict.update({"{} - {}".format(id, nombre): id for id, nombre in empleados})
        self.combo_id_empleado['values'] = list(self.empleados_dict.keys())
        self.combo_id_empleado.set("Ninguno")

    def guardar_cambios(self):
        departamento_seleccionado = self.combo_departamento.get()
        departamento_id = self.departamentos_dict.get(departamento_seleccionado)
        if not departamento_id:
            messagebox.showerror("Error", "Debe seleccionar un departamento válido para modificar.")
            return
        nuevo_nombre_departamento = self.entrada_nombre.get().strip()
        gerente_seleccionado = self.combo_id_empleado.get()
        id_gerente = self.empleados_dict.get(gerente_seleccionado)
        if not nuevo_nombre_departamento and id_gerente is None:
            messagebox.showerror("Error", "Debe modificar al menos un campo.")
            return
        try:
            crud_departamento = CRUDdepartamento()
            campos_actualizar = []
            valores = []
            if nuevo_nombre_departamento:
                campos_actualizar.append("nombre_departamento = %s")
                valores.append(nuevo_nombre_departamento)
            if gerente_seleccionado != "Ninguno":
                campos_actualizar.append("id_gerente = %s")
                valores.append(id_gerente)
            else:
                campos_actualizar.append("id_gerente = %s")
                valores.append(None)
            query = f"UPDATE departamentos SET {', '.join(campos_actualizar)} WHERE id_departamentos = %s"
            valores.append(departamento_id)
            if crud_departamento.actualizar_campos(query, tuple(valores)):
                messagebox.showinfo("Éxito", "Departamento modificado correctamente.")
                self.ventana.destroy()
                self.app.cargar_departamentos()
            else:
                messagebox.showerror("Error", "No se pudo modificar el departamento.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaEliminarDepartamento:

    def __init__(self, app: VentanaGestionDepartamentos) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Eliminar Departamento")
        self.ventana.geometry("400x200")
        Label(self.ventana, text="Seleccione el Departamento a eliminar").grid(row=0, column=0, padx=10, pady=10)
        self.combo_departamento = Combobox(self.ventana, state="readonly")
        self.combo_departamento.grid(row=0, column=1, padx=10, pady=10)
        self.cargar_departamentos()
        Button(self.ventana, text="Eliminar Departamento", command=self.eliminar_departamento).grid(row=1, column=1, pady=20, padx=10)

    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
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
            crud_departamento = CRUDdepartamento()
            if crud_departamento.reasignar_y_eliminar(departamento_id):
                messagebox.showinfo("Éxito", "Departamento eliminado correctamente.")
                self.ventana.destroy()
                self.app.cargar_departamentos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el departamento.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaVerDepartamento:
    def __init__(self, app: Programa) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Ver Departamentos y Empleados")
        self.ventana.geometry("800x600")
        Label(self.ventana, text="Departamentos").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tree_departamentos = Treeview(self.ventana, columns=("id", "nombre", "gerente"), show="headings")
        self.tree_departamentos.heading("id", text="ID Departamento")
        self.tree_departamentos.heading("nombre", text="Nombre")
        self.tree_departamentos.heading("gerente", text="Gerente")
        self.tree_departamentos.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.tree_departamentos.bind("<<TreeviewSelect>>", self.mostrar_empleados_asociados)
        Label(self.ventana, text="Empleados Asociados").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.tree_empleados = Treeview(self.ventana, columns=("id", "nombre", "salario"), show="headings")
        self.tree_empleados.heading("id", text="ID Empleado")
        self.tree_empleados.heading("nombre", text="Nombre")
        self.tree_empleados.heading("salario", text="Salario")
        self.tree_empleados.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.cargar_departamentos()

    def cargar_departamentos(self):
        crud_departamento = CRUDdepartamento()
        departamentos = crud_departamento.mostrar_departamentos_con_gerente()
        for item in self.tree_departamentos.get_children():
            self.tree_departamentos.delete(item)
        for depto in departamentos:
            id_departamento, nombre, gerente = depto
            gerente = gerente if gerente else "Sin Asignar"
            self.tree_departamentos.insert("", "end", values=(id_departamento, nombre, gerente))

    def mostrar_empleados_asociados(self, event):
        selected_item = self.tree_departamentos.selection()
        if not selected_item:
            return
        departamento_id = self.tree_departamentos.item(selected_item, "values")[0]
        for item in self.tree_empleados.get_children():
            self.tree_empleados.delete(item)
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_empleados_por_departamento(departamento_id)
        for emp in empleados:
            id_empleado, nombre, salario = emp
            self.tree_empleados.insert("", "end", values=(id_empleado, nombre, salario))

class VentanaGestionProyectos:
    def __init__(self, app: Programa) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Gestión de Proyectos")
        self.ventana.geometry("1080x700")
        marco_botones = Frame(self.ventana)
        marco_botones.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        self.boton_nuevo_proyecto = Button(marco_botones, text="Nuevo Proyecto", command=self.nuevo_proyecto)
        self.boton_nuevo_proyecto.grid(row=0, column=0, padx=20, pady=20)
        self.boton_modificar_proyecto = Button(marco_botones, text="Modificar Proyecto", command=self.modificar_proyecto)
        self.boton_modificar_proyecto.grid(row=0, column=1, padx=20, pady=20)
        self.boton_eliminar_proyecto = Button(marco_botones, text="Eliminar Proyecto", command=self.eliminar_proyecto)
        self.boton_eliminar_proyecto.grid(row=0, column=2, padx=20, pady=20)
        self.boton_actualizar = Button(self.ventana, text="Actualizar", command=self.cargar_proyectos)
        self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
        self.boton_asignar_empleado = Button(marco_botones, text="Asignar empleado a proyecto", command=self.asignar_empleado)
        self.boton_asignar_empleado.grid(row=0, column=3, padx=20, pady=20)
        columnas = ("id_proyecto", "nombre", "descripcion", "fecha_inicio")
        self.tabla_proyectos = Treeview(self.ventana, columns=columnas, show="headings")
        self.tabla_proyectos.heading("id_proyecto", text="ID Proyecto")
        self.tabla_proyectos.heading("nombre", text="Nombre")
        self.tabla_proyectos.heading("descripcion", text="Descripción")
        self.tabla_proyectos.heading("fecha_inicio", text="Fecha Inicio")
        self.tabla_proyectos.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.cargar_proyectos()

    def cargar_proyectos(self):
        try:
            for item in self.tabla_proyectos.get_children():
                self.tabla_proyectos.delete(item)
            crud_proyectos = CRUDproyecto()
            proyectos = crud_proyectos.obtener()
            if proyectos:
                for p in proyectos:
                    id_proyectos, nombre_proyecto, descripcion_proyecto, fecha_inicio_proyecto = p
                    self.tabla_proyectos.insert("", "end", values=(
                        id_proyectos, nombre_proyecto, descripcion_proyecto, fecha_inicio_proyecto
                    ))
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar proyectos: {}".format(e))

    def nuevo_proyecto(self):
        VentanaNuevoProyecto(self)

    def modificar_proyecto(self):
        VentanaModificarProyecto(self)

    def eliminar_proyecto(self):
        VentanaEliminarProyecto(self)
    def asignar_empleado(self):
        VentanaAsignarEmpleado(self)

class VentanaNuevoProyecto:

    def __init__(self, app: VentanaGestionProyectos) -> None:
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
            crud_proyectos = CRUDproyecto()
            proyecto = Proyecto(nombre_proyecto,descripcion,fecha_inicio)
            if crud_proyectos.insertar(proyecto):
                messagebox.showinfo("Éxito", "Proyecto creado correctamente.")
                self.ventana.destroy()
                self.app.cargar_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo crear el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaModificarProyecto:

    def __init__(self, app: VentanaGestionDepartamentos) -> None:
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
        self.cargar_proyectos()

    def cargar_proyectos(self):
        crud_proyectos = CRUDproyecto()
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
            crud_proyectos = CRUDproyecto()
            query = f"UPDATE proyectos SET {', '.join(campos_actualizar)} WHERE id_proyectos = %s"
            if crud_proyectos.actualizar_campos(query, tuple(valores)):
                messagebox.showinfo("Éxito", "Proyecto modificado correctamente.")
                self.ventana.destroy()
                self.app.cargar_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo modificar el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

class VentanaEliminarProyecto:

    def __init__(self, app: VentanaGestionProyectos) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Eliminar Proyecto")
        self.ventana.geometry("400x200")
        Label(self.ventana, text="Seleccione el Proyecto a eliminar").grid(row=0, column=0, padx=10, pady=10)
        self.combo_proyecto = Combobox(self.ventana, state="readonly")
        self.combo_proyecto.grid(row=0, column=1, padx=10, pady=10)
        self.cargar_proyectos()
        Button(self.ventana, text="Eliminar Proyecto", command=self.eliminar_proyecto).grid(row=1, column=1, pady=20, padx=10)

    def cargar_proyectos(self):
        crud_proyectos = CRUDproyecto()
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
            crud_proyecto = CRUDproyecto()
            if crud_proyecto.eliminar(proyecto_id):
                messagebox.showinfo("Éxito", "Proyecto eliminado correctamente.")
                self.ventana.destroy()
                self.app.cargar_proyectos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el proyecto.")
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error: {}".format(e))

class VentanaAsignarEmpleado:
    def __init__(self, app: VentanaGestionProyectos) -> None:
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
            self.cargar_empleados()
            self.cargar_proyectos()

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        if not empleados:
            self.empleados_dict = {"Ninguno": None}
            self.combo_id_empleado['values'] = ["Ninguno"]
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre): id for id, nombre in empleados}
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())

    def cargar_proyectos(self):
        crud_proyectos = CRUDproyecto()
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
        crud_guardar = CRUDempleado()
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

class VentanaGestionRegistros:
    def __init__(self, app: Programa, rol: str) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Gestión de Registro Tiempo")
        self.ventana.geometry("1700x700")
        marco_botones = Frame(self.ventana)
        marco_botones.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="w")
        self.boton_nuevo_registro = Button(marco_botones, text="Nuevo Registro", command=self.nuevo_registro)
        self.boton_nuevo_registro.grid(row=0, column=0, padx=20, pady=20)
        self.boton_modificar_registro = Button(marco_botones, text="Modificar Registro", command=self.modificar_registro)
        self.boton_modificar_registro.grid(row=0, column=1, padx=20, pady=20)
        self.boton_eliminar_registro = Button(marco_botones, text="Eliminar Registro", command=self.eliminar_registro)
        self.boton_eliminar_registro.grid(row=0, column=2, padx=20, pady=20)
        self.boton_actualizar = Button(self.ventana, text="Actualizar", command=self.cargar_registro)
        self.boton_actualizar.grid(row=3, column=0, padx=20, pady=20)
        columnas = ("id_registro_tiempo", "fecha_registro", "cantidad_horas_trabajadas", "descripcion", "proyectos_id", "empleados_id_empleado")
        self.tabla_registros = Treeview(self.ventana, columns=columnas, show="headings")
        self.tabla_registros.heading("id_registro_tiempo", text="ID Registro Tiempo")
        self.tabla_registros.heading("fecha_registro", text="Fecha Registro")
        self.tabla_registros.heading("cantidad_horas_trabajadas", text="Horas Trabajadas")
        self.tabla_registros.heading("descripcion", text="Descripción")
        self.tabla_registros.heading("proyectos_id", text="ID Proyecto")
        self.tabla_registros.heading("empleados_id_empleado", text="ID Empleado")
        self.tabla_registros.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.cargar_registro()

        if rol == "usuario":
            self.esconder_botones_usuario()

    def nuevo_registro(self):
        VentanaNuevoRegistro(self)

    def modificar_registro(self):
        VentanaModificarRegistro(self)

    def eliminar_registro(self):
        VentanaEliminarRegistro(self)
            
    def cargar_registro(self):
        for item in self.tabla_registros.get_children():
            self.tabla_registros.delete(item)
        try:
            crud_registro = CRUDRegistroTiempo()
            registros = crud_registro.mostrar_todos()
            if registros:
                for registro in registros:
                    self.tabla_registros.insert("", "end", values=(
                        registro[0],  
                        registro[1], 
                        registro[2], 
                        registro[3],  
                        registro[4],  
                        registro[5]   
                    ))
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar registros de tiempo: {}".format(e))
    
    def esconder_botones_usuario(self):
        self.boton_modificar_registro.grid_forget()
        self.boton_eliminar_registro.grid_forget()

class VentanaNuevoRegistro:

    def __init__(self, app: VentanaGestionRegistros) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Ingreso Registro de Tiempo")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="ID Empleado").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=0, column=1, padx=10, pady=5)
        Label(self.ventana, text="Proyecto").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.combo_proyecto = Combobox(self.ventana, state="readonly")
        self.combo_proyecto.grid(row=1, column=1, padx=10, pady=5)
        Label(self.ventana, text="Fecha (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=2, column=1, padx=10, pady=10)
        Label(self.ventana, text="Descripción").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.entrada_descripcion = Entry(self.ventana)
        self.entrada_descripcion.grid(row=3, column=1, padx=10, pady=5)
        Label(self.ventana, text="Horas Trabajadas").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entrada_horas = Entry(self.ventana)
        self.entrada_horas.grid(row=4, column=1, padx=10, pady=5)
        Button(self.ventana, text="Ingresar Registro", command=self.guardar_cambios).grid(row=5, column=1, pady=20, padx=10)
        self.cargar_empleados()
        self.cargar_proyectos()

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        if not empleados:
            self.empleados_dict = {"Ninguno": None}
            self.combo_id_empleado['values'] = ["Ninguno"]
        else:
            self.empleados_dict = {"{} - {}".format(id, nombre): id for id, nombre in empleados}
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())
            self.combo_id_empleado.set("Seleccione un empleado")
        
    def cargar_proyectos(self):
        crud_proyectos = CRUDproyecto()
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
        crud_guardar = CRUDRegistroTiempo()
        descripcion = self.entrada_descripcion.get()
        cantidad_horas = self.entrada_horas.get()
        fecha = self.entrada_fecha_inicio.get()
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
        registro = RegistroTiempo(fecha,cantidad_horas,descripcion,proyecto_id,empleado_id)
        try:
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            cantidad_horas = int(cantidad_horas)
        except ValueError:
            messagebox.showerror("Error", "Formato incorrecto para fecha o cantidad de horas.")
            return
        crud_guardar.insertar(registro)
        if crud_guardar:
            messagebox.showinfo("Éxito", "Registro guardado correctamente.")
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo guardar registro.") 


class VentanaModificarRegistro:
    def __init__(self, app: VentanaGestionRegistros) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Modificar Registro de Tiempo")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="ID Registro de Tiempo").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_registro = Combobox(self.ventana, state="readonly")
        self.combo_id_registro.grid(row=0, column=1, padx=10, pady=5)
        
        Label(self.ventana, text="Empleado").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_empleado = Combobox(self.ventana, state="readonly")
        self.combo_id_empleado.grid(row=1, column=1, padx=10, pady=5)

        Label(self.ventana, text="Proyecto").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.combo_proyecto = Combobox(self.ventana, state="readonly")
        self.combo_proyecto.grid(row=2, column=1, padx=10, pady=5)

        Label(self.ventana, text="Fecha (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=10)
        self.entrada_fecha_inicio = Entry(self.ventana)
        self.entrada_fecha_inicio.grid(row=3, column=1, padx=10, pady=10)

        Label(self.ventana, text="Descripción").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entrada_descripcion = Entry(self.ventana)
        self.entrada_descripcion.grid(row=4, column=1, padx=10, pady=5)

        Label(self.ventana, text="Horas Trabajadas").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entrada_horas = Entry(self.ventana)
        self.entrada_horas.grid(row=5, column=1, padx=10, pady=5)

        Button(self.ventana, text="Guardar Cambios", command=self.guardar_cambios).grid(row=6, column=1, pady=20, padx=10)

        self.cargar_registros()
        self.cargar_empleados()
        self.cargar_proyectos()

    def cargar_registros(self):
        crud_registro = CRUDRegistroTiempo()
        registros = crud_registro.obtener_todos()
        if not registros:
            self.registros_dict = {"Ninguno": None}
            self.combo_id_registro["values"] = ["Ninguno"]
        else:
            self.registros_dict = {"{} - {}".format(id_registro, descripcion): id_registro for id_registro, descripcion, in registros}
            self.combo_id_registro["values"] = list(self.registros_dict.keys())
            self.combo_id_registro.set("Seleccione un registro")

    def cargar_empleados(self):
        crud_empleado = CRUDempleado()
        empleados = crud_empleado.obtener_todos()
        self.empleados_dict = {"Ninguno": None}
        if empleados:
            self.empleados_dict.update({"{} - {}".format(id, nombre): id for id, nombre in empleados})
            self.combo_id_empleado['values'] = list(self.empleados_dict.keys())
            self.combo_id_empleado.set("Ninguno")

    def cargar_proyectos(self):
        crud_proyectos = CRUDproyecto()
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
        try:
            registro_seleccionado = self.combo_id_registro.get()
            registro_id = self.registros_dict.get(registro_seleccionado)
            if not registro_id:
                messagebox.showerror("Error", "Seleccione un registro válido.")
                return
            
            campos_registro = {}
            if self.combo_id_empleado.get().strip():
                empleado_seleccionado = self.combo_id_empleado.get()
                campos_registro['empleados_id_empleado'] = self.empleados_dict.get(empleado_seleccionado)
            if self.combo_proyecto.get().strip():
                proyecto_seleccionado = self.combo_proyecto.get()
                campos_registro['proyectos_id'] = self.proyectos_dict.get(proyecto_seleccionado)
            if self.entrada_fecha_inicio.get().strip():
                campos_registro['fecha_registro'] = datetime.strptime(self.entrada_fecha_inicio.get().strip(), "%Y-%m-%d")
            if self.entrada_descripcion.get().strip():
                campos_registro['descripcion'] = self.entrada_descripcion.get().strip()
            if self.entrada_horas.get().strip():
                campos_registro['cantidad_horas_trabajadas'] = int(self.entrada_horas.get().strip())
            
            crud = CRUDRegistroTiempo()
            actualizado = crud.actualizar(registro_id, campos_registro)
            if actualizado:
                messagebox.showinfo("Éxito", "Registro modificado correctamente.")
                self.ventana.destroy()
                self.app.cargar_registros()
            else:
                messagebox.showerror("Error", "No se pudo modificar el registro.")
        except ValueError as e:
            messagebox.showerror("Error de Entrada", "Formato de entrada incorrecto: {}".format(e))
        except Exception as e:
            messagebox.showerror("Error", "Ocurrió un error inesperado: {}".format(e))



class VentanaEliminarRegistro:
    def __init__(self, app: VentanaGestionRegistros) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana) 
        self.ventana.title("Eliminar Registro de Tiempo")   
        self.ventana.geometry("500x500")
        Label(self.ventana, text="ID Registro de tiempo").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.combo_id_registro = Combobox(self.ventana, state="readonly")
        self.combo_id_registro.grid(row=0, column=1, padx=10, pady=5)
        self.cargar_registros()
        Button(self.ventana, text="Eliminar", command=self.eliminar_registro).grid(row=1, column=1, pady=20, padx=10)

    def cargar_registros(self):
        CRUDregistro = CRUDRegistroTiempo()
        registro = CRUDregistro.mostrar_id_registro()
        if not registro:
            self.registro_dict = {"Ninguno": None}
            self.combo_id_registro["values"] = ["Ninguno"]
        else:
            self.combo_id_registro["values"] = registro

    def eliminar_registro(self):
        print("¡Botón presionado!")
        CRUDregistro = CRUDRegistroTiempo()
        id_registro = self.combo_id_registro.get()
        if id_registro == id_registro:
            try:
                id_registro = int(id_registro)
                exito = CRUDregistro.eliminar(id_registro)
                if exito:
                    print(f"Registro con ID {id_registro} eliminado correctamente.")
                    self.ventana.destroy()
                    self.app.cargar_registros()
                else:
                    print(f"No se pudo eliminar el registro con ID {id_registro}.")
            except ValueError:
                print("Por favor, selecciona un ID válido (número).")
            except Exception as e:
                print(f"Error inesperado: {e}")
        else:
            print("No se seleccionó ninguna ID de registro.")

class VentanaConsultaIndicadores:
    def __init__(self, app: Programa) -> None:
        self.app = app
        self.ventana = Toplevel(self.app.ventana)
        self.ventana.title("Consulta de Indicadores Económicos")
        self.ventana.geometry("600x500")
        Label(self.ventana, text="Indicador:").grid(row=0, column=0, padx=10, pady=10)
        self.combo_indicadores = Combobox(self.ventana, state="readonly")
        self.combo_indicadores.grid(row=0, column=1, padx=10, pady=10)
        Label(self.ventana, text="Unidad de Medida: Pesos Chilenos").grid(row=0, column=2, padx=10, pady=10)
        Label(self.ventana, text="Fecha(DD-MM-YYYY):").grid(row=1, column=0, padx=10, pady=10)
        self.entrada_fecha = Entry(self.ventana)
        self.entrada_fecha.grid(row=1, column=1, padx=10, pady=10)
        self.resultado_label = Label(self.ventana, text="Resultado: ")
        self.resultado_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.indicador_label = Label(self.ventana, text="Indicador: ")
        self.indicador_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        self.fecha_label = Label(self.ventana, text="Fecha: ")
        self.fecha_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.valor_label = Label(self.ventana, text="Valor: ")
        self.valor_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.origen_label = Label(self.ventana, text="Origen: ")
        self.origen_label.grid(row=6, column=0, columnspan=1, padx=0, pady=10)
        self.vacio_label1 = Label(self.ventana, text="")
        self.vacio_label1.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        self.vacio_label2 = Label(self.ventana, text="")
        self.vacio_label2.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.vacio_label3 = Label(self.ventana, text="")
        self.vacio_label3.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
        self.vacio_label4 = Label(self.ventana, text="")
        self.vacio_label4.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
        Button(self.ventana, text="Cargar Indicador", command=self.cargar_indicador).grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.usuario_label = Label(self.ventana, text="Usuario:")
        self.usuario_label.grid(row=8, column=0, padx=10, pady=10)
        self.entrada_usuario = Entry(self.ventana)
        self.entrada_usuario.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        Button(self.ventana, text="Registrar Informacion", command=self.registrar_informacion).grid(row=9, column=0, columnspan=3, padx=10, pady=10)
        self.cargar_indicadores_combo()
    
    def cargar_indicadores_combo(self):
        indiciadores = [
        (1, "uf"),
        (2, "ivp"),
        (3, "ipc"),
        (4, "utm"),
        (5, "dolar"),
        (6, "euro")
        ]
        self.indicadores_dict = {nombre: id for id, nombre in indiciadores}
        self.combo_indicadores['values'] = list(self.indicadores_dict.keys())
    
    def cargar_indicador(self):
        ind = MiIndicador()
        indicador = self.combo_indicadores.get()
        fecha = self.entrada_fecha.get()
        if not indicador or not fecha:
            messagebox.showinfo("Error", "Debe completar todos los campos.")
            return
        datos, url = ind.fetch_indicador(indicador, fecha)
        if datos:
            try:
                valor = datos['serie'][0]['valor']
                self.vacio_label1.config(text=f"{indicador.upper()}")
                self.vacio_label2.config(text=f"{fecha}")
                self.vacio_label3.config(text=f"{valor}")
                self.vacio_label4.config(text=f"{url}")
            except KeyError:
                messagebox.showerror("Error", "No se pudo obtener el valor.")
                self.resultado_label.config(text="Error: No se pudo obtener el valor.", fg="red")
                self.resultado_label.after(3000, lambda: self.resultado_label.config(text="Resultado: ", fg="black"))
            except IndexError:
                messagebox.showerror("Error", "El valor no se puede encontrar en esta fecha.")
                self.resultado_label.config(text="Error: El valor no se puede encontrar en esta fecha.", fg="red")
                self.resultado_label.after(3000, lambda: self.resultado_label.config(text="Resultado: ", fg="black"))
        else:
            self.resultado_label.config(text="Error: No se pudo obtener el valor.", fg="red")
            self.resultado_label.after(3000, lambda: self.resultado_label.config(text="Resultado: ", fg="black"))

    def registrar_informacion(self):
        ind = MiIndicador()
        crud = CRUDempleado()
        indicador = self.combo_indicadores.get()
        fecha = self.entrada_fecha.get()
        usuario = self.entrada_usuario.get()
        _, url = ind.fetch_indicador(indicador,fecha)
        if crud.obtener_por_nombre(usuario) == None:
            messagebox.showerror("Error", "No se ha encontrado el usuario para ser usado.")
        if usuario == "":
            messagebox.showinfo("Info", "Es necesario que para hacer el registro, el campo de usuario este rellenado.")
        elif crud.registro_informacion(indicador, usuario, fecha, url) == True:
            messagebox.showinfo("Exito", "El registro se ha creado exitosamente.")
        

# Inicialización de la aplicación
root = Tk()
app = PantallaLogin(root)
root.mainloop()