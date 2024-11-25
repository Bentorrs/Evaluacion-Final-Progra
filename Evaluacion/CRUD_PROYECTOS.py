from mysql.connector import MySQLConnection, connect, Error
from datetime import datetime
from Modelo_Final import Proyecto

class CRUDproyecto:
    def __init__(self) -> None:
        
        self.username = 'root'
        self.password = ''
        self.database = 'ecotechsoluciones'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def insertar(self, proyecto: Proyecto) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM proyectos WHERE nombre_proyecto = %s"
            cursor.execute(query_check, (proyecto.nombre_proyecto,))
            proyecto_existe = cursor.fetchone()
            if proyecto_existe:
                return False
            query = "INSERT INTO proyectos (nombre_proyecto, descripcion_proyecto, fecha_inicio_proyecto) VALUES (%s, %s, %s);"
            values = (proyecto.nombre_proyecto, proyecto.descripcion_proyecto, proyecto.fecha_inicio)
            cursor.execute(query, values)
            cnx.commit()
            return True
        except Error as e:
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_todos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT * FROM proyectos;"
            cursor.execute(query)
            proyectos = cursor.fetchall()
            if proyectos:
                for proyecto in proyectos:
                    print("ID: {}, Nombre: {}, Descripción: {}, Fecha de Inicio: {}".format(
                        proyecto[0], proyecto[1], proyecto[2], proyecto[3]))
            else:
                print("No se encontraron proyectos en la base de datos.")
        except Error as e:
            print("Error al mostrar todos los proyectos: {}".format(e))
        finally:
            cursor.close()

    def obtener(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT * FROM proyectos;"
            cursor.execute(query)
            proyectos = cursor.fetchall()
            if proyectos:
                return proyectos
            else:
                print("No se encontraron proyectos en la base de datos.")
        except Error as e:
            print("Error al mostrar todos los proyectos: {}".format(e))
        finally:
            cursor.close()

    def mostrar_por_id(self, id_proyecto: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT * FROM proyectos WHERE id_proyecto = %s;"
            cursor.execute(query, (id_proyecto,))
            proyecto = cursor.fetchone()
            if proyecto:
                print("ID: {}, Nombre: {}, Descripción: {}, Fecha de Inicio: {}".format(
                    proyecto[0], proyecto[1], proyecto[2], proyecto[3]))
                return proyecto
            else:
                print("No se encontró el proyecto con ID {}.".format(id_proyecto))
                return None
        except Error as e:
            print("Error al mostrar proyecto por ID: {}".format(e))
        finally:
            cursor.close()

    def modificar(self, id_proyecto: int, nuevo_nombre: str, nueva_descripcion: str, nueva_fecha_inicio: datetime) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM proyectos WHERE id_proyecto = %s"
            cursor.execute(query_check, (id_proyecto,))
            proyecto_existe = cursor.fetchone()
            if not proyecto_existe:
                print("No se encontró el proyecto con ID {} para modificar.".format(id_proyecto))
                return False
            query_update = """
            UPDATE proyectos 
            SET nombre_proyecto = %s, descripcion_proyecto = %s, fecha_inicio_proyecto = %s 
            WHERE id_proyecto = %s;
            """
            values = (nuevo_nombre, nueva_descripcion, nueva_fecha_inicio, id_proyecto)
            cursor.execute(query_update, values)
            cnx.commit()
            print("Proyecto con ID {} modificado correctamente.".format(id_proyecto))
            return True
        except Error as e:
            print("Error al modificar proyecto: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def eliminar(self, id_proyectos: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM proyectos WHERE id_proyectos = %s"
            cursor.execute(query_check, (id_proyectos,))
            proyecto_existe = cursor.fetchone()
            if not proyecto_existe:
                print("No se encontró el proyecto con ID {} para eliminar.".format(id_proyectos))
                return False
            query_delete = "DELETE FROM proyectos WHERE id_proyectos = %s;"
            cursor.execute(query_delete, (id_proyectos,))
            cnx.commit()
            print("Proyecto con ID {} eliminado correctamente.".format(id_proyectos))
            return True
        except Error as e:
            print("Error al eliminar proyecto: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def actualizar_campos(self, query, valores):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            cursor.execute(query, valores)
            cnx.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al actualizar departamento: {e}")
            cnx.rollback()
            return False

# crud = CRUDproyecto()
# nuevo = Proyecto("X-Men", "Mutantes del espacio", datetime(2024,10,26))
# crud.insertar(nuevo)

# crud.mostrar_todos()