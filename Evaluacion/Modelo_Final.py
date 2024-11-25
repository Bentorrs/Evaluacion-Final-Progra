from datetime import datetime

class Usuario:
    def __init__(self, nombre_usuario: str, contrasenna: str, es_admin: bool) -> None:
        self.nombre_usuario = nombre_usuario
        self.contrasenna = contrasenna
        self.es_admin = es_admin
    

class Empleado(Usuario):
    def __init__(self, nombre_usuario: str, contrasenna: str, es_admin: bool, nombre_empleado: str, 
        direccion_empleado: str, numero_telefono: str, correo_electronico_empleado: str, 
        salario_empleado: int, fecha_inicio_contrato: datetime, departamentos_id_departamentos: int) -> None:
        super().__init__(nombre_usuario, contrasenna, es_admin)
        self.nombre_empleado = nombre_empleado
        self.direccion_empleado = direccion_empleado
        self.numero_telefono = numero_telefono
        self.correo_electronico_empleado = correo_electronico_empleado
        self.salario_empleado = salario_empleado
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.departamentos_id_departamentos = departamentos_id_departamentos

class Departamento:

    def __init__(self, nombre_departamento: str) -> None:
        self.nombre_departamento = nombre_departamento

class Proyecto:
    
    def __init__(self, nombre_proyecto: str, descripcion_proyecto: str, fecha_inicio: datetime) -> None:
        self.nombre_proyecto = nombre_proyecto
        self.descripcion_proyecto = descripcion_proyecto
        self.fecha_inicio = fecha_inicio

class RegistroTiempo:

    def __init__(self, fecha_registro: datetime, cantidad_horas_trabajadas: int, descripcion: str, proyectos_id: int, empleados_id_empleado: int) -> None:
        self.fecha_registro = fecha_registro
        self.cantidad_horas_trabajadas = cantidad_horas_trabajadas
        self.descripcion = descripcion
        self.proyectos_id = proyectos_id
        self.empleados_id_empleado = empleados_id_empleado

class ProyectosHasEmpleados:

    def __init__(self, proyectos_id_proyectos: int, id_empleado: int) -> None:
        self.proyectos_id_proyectos = proyectos_id_proyectos
        self.id_empleado = id_empleado 