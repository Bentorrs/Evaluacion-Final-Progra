import mysql.connector
from datetime import datetime
from modelo import Tiempo

class crud_tiempo:
    def conectar() -> mysql.connector.MySQLConnection:
        try:
            cnx = mysql.connector.connect(
                username='root',
                password='',
                database='gestion_empleados')
            return cnx
        except ValueError:
            print("Error de conexión")
            return None

    def insertar(self, registro) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """INSERT INTO registro_tiempo (fecha_registro, cantidad_horas_trabajadas, descripcion, proyectos_id, empleados_id_empleado)
                    VALUES (%s, %s, %s, %s, %s);"""
            values = (registro.fecha_registro, registro.cantidad_horas_trabajadas, registro.descripcion, 
                    registro.proyectos_id, registro.empleados_id_empleado)
            cursor.execute(query, values)
            cnx.commit()
            print("Registro de tiempo insertado correctamente.")
            return True
        except ValueError as e:
            print("Error al insertar registro de tiempo: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_todos(self):
            try:
                cnx = self.conectar()
                cursor = cnx.cursor()
                query = "SELECT id_registro_tiempo, fecha_registro, cantidad_horas_trabajadas, descripcion, proyectos_id, empleados_id_empleado FROM registro_tiempo;"
                cursor.execute(query)
                registros = cursor.fetchall()
                return registros
            except Exception as e:
                print("Error al mostrar todos los registros de tiempo:", e)
                return []
            finally:
                cursor.close()

    def mostrar_por_id(self, id_registro: int):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT * FROM registro_tiempo WHERE id_registro_tiempo = %s;"
            cursor.execute(query, (id_registro,))
            registro = cursor.fetchone()
            if registro:
                print("ID: {}, Fecha: {}, Horas Trabajadas: {}, Descripción: {}, ID Proyecto: {}, ID Empleado: {}".format(
                    registro[0], registro[1], registro[2], registro[3], registro[4], registro[5]))
                return registro
            else:
                print("No se encontró el registro de tiempo con ID {}.".format(id_registro))
                return None
        except ValueError as e:
            print("Error al mostrar registro de tiempo por ID: {}".format(e))
        finally:
            cursor.close()
    
    def mostrar_id_registro(self):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT DISTINCT id_registro_tiempo FROM registro_tiempo;"
            cursor.execute(query)
            id_registro = [row[0] for row in cursor.fetchall()]
            print(id_registro)
            return id_registro
        except ValueError:
            print("Error")
        finally:
            cursor.close()

    def modificar(self, id_registro: int, nueva_fecha: datetime, nuevas_horas: int, nueva_descripcion: str, 
                    nuevo_proyecto_id: int, nuevo_empleado_id: int) -> bool:
        try:
            cursor = self.cnx.cursor()
            query_check = "SELECT 1 FROM registro_tiempo WHERE id_registro_tiempo = %s"
            cursor.execute(query_check, (id_registro,))
            registro_existe = cursor.fetchone()
            if not registro_existe:
                print("No se encontró el registro de tiempo con ID {} para modificar.".format(id_registro))
                return False
            query_update = """
            UPDATE registro_tiempo 
            SET fecha_registro = %s, cantidad_horas_trabajadas = %s, descripcion = %s, 
                proyectos_id = %s, empleados_id_empleado = %s 
            WHERE id_registro_tiempo = %s;
            """
            values = (nueva_fecha, nuevas_horas, nueva_descripcion, nuevo_proyecto_id, nuevo_empleado_id, id_registro)
            cursor.execute(query_update, values)
            self.cnx.commit()
            print("Registro de tiempo con ID {} modificado correctamente.".format(id_registro))
            return True
        except ValueError as e:
            print("Error al modificar registro de tiempo: {}".format(e))
            if self.cnx.is_connected():
                self.cnx.rollback()
            return False
        finally:
            cursor.close()

    def eliminar(self, id_registro: int) -> bool:
        try:
            cursor = self.cnx.cursor()
            query_check = "SELECT 1 FROM registro_tiempo WHERE id_registro_tiempo = %s"
            cursor.execute(query_check, (id_registro,))
            registro_existe = cursor.fetchone()
            if not registro_existe:
                print("No se encontró el registro de tiempo con ID {} para eliminar.".format(id_registro))
                return False
            query_delete = "DELETE FROM registro_tiempo WHERE id_registro_tiempo = %s;"
            cursor.execute(query_delete, (id_registro,))
            self.cnx.commit()
            print("Registro de tiempo con ID {} eliminado correctamente.".format(id_registro))
            return True
        except ValueError as e:
            print("Error al eliminar registro de tiempo: {}".format(e))
            if self.cnx.is_connected():
                self.cnx.rollback()
            return False
        finally:
            cursor.close()

