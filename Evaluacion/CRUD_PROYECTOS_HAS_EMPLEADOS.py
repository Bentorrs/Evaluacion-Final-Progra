from mysql.connector import MySQLConnection, connect, Error
from datetime import datetime
from Modelo_Final import ProyectosHasEmpleados

class Conexion:
    def __init__(self) -> None:
        self.host = "localhost"
        self.username = "root"
        self.password = ""
        self.database = "ecotechsoluciones"

    def conectar(self) -> MySQLConnection:
        try:
            cnx = connect(
                host=self.host, 
                user=self.username,
                password=self.password, 
                database=self.database
            )
            return cnx
        except Error as e:
            print("Error de conexión: {}".format(e))
            return None

class CRUDProyectosHasEmpleados:
    def __init__(self) -> None:
        self.conexion = Conexion().conectar()

    def asignar_empleado_a_proyecto(self, id_proyecto: int, id_empleado: int) -> bool:
        try:
            cursor = self.conexion.cursor()
            query_check_proyecto = "SELECT 1 FROM proyectos WHERE id_proyectos = %s"
            cursor.execute(query_check_proyecto, (id_proyecto,))
            proyecto_existe = cursor.fetchone()
            query_check_empleado = "SELECT 1 FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_check_empleado, (id_empleado,))
            empleado_existe = cursor.fetchone()
            if not proyecto_existe:
                print("Error: No existe un proyecto con ID '{}'.".format(id_proyecto))
                return False
            if not empleado_existe:
                print("Error: No existe un empleado con ID '{}'.".format(id_empleado))
                return False
            query = """
            INSERT INTO proyectos_has_empleados (proyectos_id_proyectos, id_empleado)
            VALUES (%s, %s);
            """
            cursor.execute(query, (id_proyecto, id_empleado))
            self.conexion.commit()
            print("Empleado asignado al proyecto correctamente.")
            return True
        except Error as e:
            print("Error al asignar empleado a proyecto: {}".format(e))
            if self.conexion.is_connected():
                self.conexion.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_todas_asignaciones(self):
        try:
            cursor = self.conexion.cursor()
            query = """
            SELECT p.id_proyectos, p.nombre_proyecto, e.id_empleado, e.nombre_empleado 
            FROM proyectos_has_empleados phe
            JOIN proyectos p ON phe.proyectos_id_proyectos = p.id_proyectos
            JOIN empleados e ON phe.id_empleado = e.id_empleado;
            """
            cursor.execute(query)
            asignaciones = cursor.fetchall()
            if asignaciones:
                for asignacion in asignaciones:
                    print("ID Proyecto: {}, Nombre Proyecto: {}, ID Empleado: {}, Nombre Empleado: {}".format(
                        asignacion[0], asignacion[1], asignacion[2], asignacion[3]))
            else:
                print("No se encontraron asignaciones de empleados a proyectos.")
        except Error as e:
            print("Error al mostrar todas las asignaciones: {}".format(e))
        finally:
            cursor.close()

    def mostrar_asignaciones_por_proyecto(self, id_proyecto: int):
        try:
            cursor = self.conexion.cursor()
            query = """
            SELECT p.id_proyectos, p.nombre_proyecto, e.id_empleado, e.nombre_empleado 
            FROM proyectos_has_empleados phe
            JOIN proyectos p ON phe.proyectos_id_proyectos = p.id_proyectos
            JOIN empleados e ON phe.id_empleado = e.id_empleado
            WHERE p.id_proyectos = %s;
            """
            cursor.execute(query, (id_proyecto,))
            asignaciones = cursor.fetchall()
            if asignaciones:
                for asignacion in asignaciones:
                    print("ID Proyecto: {}, Nombre Proyecto: {}, ID Empleado: {}, Nombre Empleado: {}".format(
                        asignacion[0], asignacion[1], asignacion[2], asignacion[3]))
            else:
                print("No se encontraron asignaciones para el proyecto con ID {}.".format(id_proyecto))
        except Error as e:
            print("Error al mostrar asignaciones del proyecto: {}".format(e))
        finally:
            cursor.close()

    def mostrar_proyectos_por_empleado(self, id_empleado: int):
        try:
            cursor = self.conexion.cursor()
            query = """
            SELECT p.id_proyectos, p.nombre_proyecto, p.descripcion_proyecto 
            FROM proyectos_has_empleados phe
            JOIN proyectos p ON phe.proyectos_id_proyectos = p.id_proyectos
            WHERE phe.id_empleado = %s;
            """
            cursor.execute(query, (id_empleado,))
            proyectos = cursor.fetchall()
            if proyectos:
                print("Proyectos asociados al empleado con ID {}:".format(id_empleado))
                for proyecto in proyectos:
                    print("ID Proyecto: {}, Nombre Proyecto: {}, Descripción: {}".format(
                        proyecto[0], proyecto[1], proyecto[2]))
            else:
                print("No se encontraron proyectos asociados al empleado con ID {}.".format(id_empleado))
        except Error as e:
            print("Error al mostrar proyectos del empleado: {}".format(e))
        finally:
            cursor.close()

    def eliminar_asignacion(self, id_proyecto: int, id_empleado: int) -> bool:
        try:
            cursor = self.conexion.cursor()
            query_check = """
            SELECT 1 FROM proyectos_has_empleados
            WHERE proyectos_id_proyectos = %s AND id_empleado = %s
            """
            cursor.execute(query_check, (id_proyecto, id_empleado))
            asignacion_existe = cursor.fetchone()
            if not asignacion_existe:
                print("No se encontró una asignación para el proyecto con ID {} y el empleado con ID {}.".format(id_proyecto, id_empleado))
                return False
            query_delete = """
            DELETE FROM proyectos_has_empleados 
            WHERE proyectos_id_proyectos = %s AND id_empleado = %s;
            """
            cursor.execute(query_delete, (id_proyecto, id_empleado))
            self.conexion.commit()
            print("Asignación eliminada correctamente.")
            return True
        except Error as e:
            print("Error al eliminar la asignación: {}".format(e))
            if self.conexion.is_connected():
                self.conexion.rollback()
            return False
        finally:
            cursor.close()

# crud = CRUDProyectosHasEmpleados()
# # crud.asignar_empleado_a_proyecto(2,12)

# # crud.mostrar_asignaciones_por_proyecto(2)
# crud.mostrar_proyectos_por_empleado(11)