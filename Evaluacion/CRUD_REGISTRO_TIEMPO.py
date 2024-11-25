from mysql.connector import MySQLConnection, connect, Error
from datetime import datetime
from Modelo_Final import RegistroTiempo

class CRUDRegistroTiempo:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'ecotechsoluciones'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def insertar(self, registro) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            INSERT INTO registro_tiempo (fecha_registro, cantidad_horas_trabajadas, descripcion, proyectos_id, empleados_id_empleado)
            VALUES (%s, %s, %s, %s, %s);
            """
            values = (registro.fecha_registro, registro.cantidad_horas_trabajadas, registro.descripcion, 
            registro.proyectos_id, registro.empleados_id_empleado)
            cursor.execute(query, values)
            cnx.commit()
            print("Registro de tiempo insertado correctamente.")
            return True
        except Error as e:
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

    def obtener_todos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT id_registro_tiempo, descripcion FROM registro_tiempo;"
            cursor.execute(query)
            registro_tiempo = cursor.fetchall()
            cursor.close()
            return registro_tiempo
        except Exception as e:
            print(f"Error al obtener registro de tiempo: {e}")
            return []

    def mostrar_por_id(self, id_registro: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
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
        except Error as e:
            print("Error al mostrar registro de tiempo por ID: {}".format(e))
        finally:
            cursor.close()
    
    def mostrar_id_registro(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT DISTINCT id_registro_tiempo FROM registro_tiempo;"
            cursor.execute(query)
            id_registro = [row[0] for row in cursor.fetchall()]
            #print(id_registro)
            return id_registro
        except Error:
            print("Error")
        finally:
            cursor.close()

    def modificar(self, id_registro: int, nueva_fecha: datetime, nuevas_horas: int, nueva_descripcion: str, 
        nuevo_proyecto_id: int, nuevo_empleado_id: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx.commit()
            print("Registro de tiempo con ID {} modificado correctamente.".format(id_registro))
            return True
        except Error as e:
            print("Error al modificar registro de tiempo: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def eliminar(self, id_registro_tiempo: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM registro_tiempo WHERE id_registro_tiempo = %s"
            print(f"Ejecutando consulta de verificación para ID {id_registro_tiempo}...")
            cursor.execute(query_check, (id_registro_tiempo,))
            cursor.fetchall()
            query_delete = "DELETE FROM registro_tiempo WHERE id_registro_tiempo = %s"
            print(f"Ejecutando consulta de eliminación para ID {id_registro_tiempo}...")
            cursor.execute(query_delete, (id_registro_tiempo,))
            cnx.commit()
            print(f"Registro con ID {id_registro_tiempo} eliminado correctamente.")
            return True
        except Error as e:
            print(f"Error al eliminar registro de tiempo: {e}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
            if cnx and cnx.is_connected():
                cnx.close()
                

    def actualizar(self, id_registro_tiempo: int, campos: dict):
        try:
            set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
            query = f"UPDATE registro_tiempo SET {set_clause} WHERE id_registro_tiempo = %s"
            values = list(campos.values())
            values.append(id_registro_tiempo)
            cnx = self.conectar()
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar el registro de tiempo: {e}")
            return False



# crud = CRUDRegistroTiempo()
# crud.mostrar_id_registro()
# nuevo = RegistroTiempo(datetime(2024,10,26),8,"Sentado Frente Al PC",2,11)
# crud.insertar(nuevo)

# crud.mostrar_todos()

# crud.modificar(6,datetime(2024,10,26),8,"Nunca se supo que hizo", 2,11)
