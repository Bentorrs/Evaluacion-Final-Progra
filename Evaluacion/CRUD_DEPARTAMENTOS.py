from mysql.connector import MySQLConnection, connect, Error
from Modelo_Final import Departamento

class CRUDdepartamento:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'ecotechsoluciones'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def insertar(self, departamento: Departamento) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "INSERT INTO departamentos (nombre_departamento) VALUES (%s);"
            values = (departamento.nombre_departamento,)
            cursor.execute(query, values)
            cnx.commit()
            print("Departamento insertado correctamente.")
            return True
        except Error as e:
            print("Error al insertar departamento: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def reasignar_y_eliminar(self, id_departamento: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check_departamento = "SELECT 1 FROM departamentos WHERE id_departamentos = %s"
            cursor.execute(query_check_departamento, (id_departamento,))
            departamento_existe = cursor.fetchone()
            if not departamento_existe:
                print("No se encontró el departamento con ID {} para eliminar.".format(id_departamento))
                return False
            query_reasignar = """
            UPDATE empleados 
            SET departamentos_id_departamentos = NULL 
            WHERE departamentos_id_departamentos = %s;
            """
            cursor.execute(query_reasignar, (id_departamento,))
            cnx.commit()
            query_eliminar = "DELETE FROM departamentos WHERE id_departamentos = %s;"
            cursor.execute(query_eliminar, (id_departamento,))
            cnx.commit()
            print("Departamento eliminado y empleados reasignados a NULL correctamente.")
            return True
        except Error as e:
            print("Error al reasignar y eliminar departamento: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def modificar(self, id_departamento: int, nuevo_nombre: str) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "UPDATE departamentos SET nombre_departamento = %s WHERE id_departamentos = %s;"
            cursor.execute(query, (nuevo_nombre, id_departamento))
            cnx.commit()
            print("Departamento modificado correctamente.")
            return True
        except Error as e:
            print("Error al modificar departamento: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_por_id(self, id_departamento: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT * FROM departamentos WHERE id_departamentos = %s;"
            cursor.execute(query, (id_departamento,))
            departamento = cursor.fetchone()
            if departamento:
                print("ID: {}, Nombre: {}, ID Gerente: {}".format(
                    departamento[0], departamento[1], departamento[2]))
                return departamento
            else:
                print("No se encontró el departamento con ID {}.".format(id_departamento))
                return None
        except Error as e:
            print("Error al mostrar departamento por ID: {}".format(e))
        finally:
            cursor.close()

    def mostrar_todos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT * FROM departamentos;"
            cursor.execute(query)
            departamentos = cursor.fetchall()
            if departamentos:
                for departamento in departamentos:
                    print("ID: {}, Nombre: {}, ID Gerente: {}".format(
                        departamento[0], departamento[1], departamento[2]))
            else:
                print("No se encontraron departamentos en la base de datos.")
        except Error as e:
            print("Error al mostrar departamentos: {}".format(e))
        finally:
            cursor.close()

    def asignar_gerente_a_departamento(self, id_departamento: int, id_gerente: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check_departamento = "SELECT 1 FROM departamentos WHERE id_departamentos = %s"
            cursor.execute(query_check_departamento, (id_departamento,))
            departamento_existe = cursor.fetchone()
            query_check_empleado = "SELECT 1 FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_check_empleado, (id_gerente,))
            empleado_existe = cursor.fetchone()
            if departamento_existe and empleado_existe:
                query_update = """
                UPDATE departamentos 
                SET id_gerente = %s 
                WHERE id_departamentos = %s;
                """
                cursor.execute(query_update, (id_gerente, id_departamento))
                cnx.commit()
                print("Gerente asignado al departamento correctamente.")
                return True
            else:
                if not departamento_existe:
                    print("No se encontró el departamento con ID {}.".format(id_departamento))
                if not empleado_existe:
                    print("No se encontró el empleado con ID {}.".format(id_gerente))
                return False
        except Error as e:
            print("Error al asignar gerente al departamento: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_departamentos_con_gerente(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            SELECT d.id_departamentos, d.nombre_departamento, e.nombre_empleado AS nombre_gerente
            FROM departamentos d
            LEFT JOIN empleados e ON d.id_gerente = e.id_empleado;
            """
            cursor.execute(query)
            departamentos = cursor.fetchall()  # Obtener todos los resultados
            return departamentos
        except Error as e:
            print("Error al mostrar departamentos con gerentes: {}".format(e))
            return None
        finally:
            cursor.close()

    def obtener_departamentos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT id_departamentos, nombre_departamento FROM departamentos;"
            cursor.execute(query)
            departamentos = cursor.fetchall()
            cursor.close()
            return departamentos
        except Error as e:
            print(f"Error al obtener departamentos: {e}")
            return []

    def insertar_departamento(self, nombre_departamento, id_gerente):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            INSERT INTO departamentos (nombre_departamento, id_gerente)
            VALUES (%s, %s)
            """
            cursor.execute(query, (nombre_departamento, id_gerente))
            cnx.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al insertar departamento: {e}")
            cnx.rollback()
            return False

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

# crud = CRUDdepartamento()
# nuevo = Departamento("Ventas")
# crud.insertar(nuevo)

# crud = CRUDdepartamento()
# crud.asignar_gerente_a_departamento(8,11)

# crud = CRUDdepartamento()
# crud.mostrar_todos()

# crud = CRUDdepartamento()
# crud.reasignar_y_eliminar(8)

# crud = CRUDdepartamento()
# crud.mostrar_departamentos_con_gerente()