from datetime import datetime

class Usuario:
    def __init__(self, nombre_usuario:str, contraseña:str) -> None:
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña

class Administrador:
    def __init__(self, Empleado_id_empleado:str, nombre_admin:str) -> None:
        self.Empleado_id_empleado = Empleado_id_empleado
        self.nombre_admin = nombre_admin

class Proyecto:
    def __init__(self, nombre_proyecto:str, descripcion:str, fecha_inicio:datetime) -> None:
        self.nombre_proyecto = nombre_proyecto
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
#cambio
class Empleado:
    def __init__(self, nombre:str, direccion:str, telefono:str, correo:str, fecha_contrato:datetime, salario:int, DEPARTAMENTO_id_departamento:int) -> None:
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_contrato = fecha_contrato
        self.salario = salario
        self.DEPARTAMENTO_id_departamento = DEPARTAMENTO_id_departamento

class Departamento:
    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

class Tiempo:
    def __init__(self, fecha: datetime, horas: str, descripcion: str, id_empleado: str) -> None:
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        self.id_empleado = id_empleado

class Proyectos_Empleados:
    def __init__(self, PROYECTO_id_proyectos: int, EMPLEADO_id_empleado: int) -> None:
        self.PROYECTO_id_proyectos = PROYECTO_id_proyectos
        self.EMPLEADO_id_empleado = EMPLEADO_id_empleado