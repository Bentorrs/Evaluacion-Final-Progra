import mysql.connector
from modelo import Departamento

class crud_departamento:
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

    def insertar(self, departamento: Departamento) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "INSERT INTO departamentos (nombre_departamento) VALUES (%s);"
            values = (departamento.nombre_departamento,)
            cursor.execute(sql, values)
            cnx.commit()
            print("Departamento insertado correctamente.")
            return True
        except ValueError as a:
            print(f"Error: {a}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def reasignar_y_eliminar(self, id_departamento: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql_dep = "SELECT 1 FROM departamentos WHERE id_departamentos = %s"
            cursor.execute(sql_dep, (id_departamento,))
            departamento_valido = cursor.fetchone()
            if not departamento_valido:
                print(f"No se encontró el ID departamento:{id_departamento} para eliminar.")
                return False
            sql_upd = """UPDATE empleados 
                        SET departamentos_id_departamentos = NULL 
                        WHERE departamentos_id_departamentos = %s;"""
            cursor.execute(sql_upd, (id_departamento,))
            cnx.commit()
            sql_eliminar = "DELETE FROM departamentos WHERE id_departamentos = %s;"
            cursor.execute(sql_eliminar, (id_departamento,))
            cnx.commit()
            print("Departamento eliminado.")
            return True
        except ValueError as a:
            print(f"Error al reasignar y eliminar departamento: {a}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def modificar(self, id_departamento: int, nuevo_nombre: str) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "UPDATE departamentos SET nombre_departamento = %s WHERE id_departamentos = %s;"
            cursor.execute(sql, (nuevo_nombre, id_departamento))
            cnx.commit()
            print("Departamento modificado correctamente.")
            return True
        except ValueError as a:
            print(f"Error al modificar departamento: {a}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_por_id(self, id_departamento: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "SELECT * FROM departamentos WHERE id_departamentos = %s;"
            cursor.execute(sql, (id_departamento,))
            departamento = cursor.fetchone()
            if departamento:
                print(f"ID: {departamento[0]}, Nombre: {departamento[1]}, ID Gerente: {departamento[2]}")
                return departamento
            else:
                print(f"No se encontró el ID departamento: {id_departamento}.")
                return None
        except ValueError as a:
            print(f"Error al mostrar departamento por ID: {a}")
        finally:
            cursor.close()

    def mostrar_todos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "SELECT * FROM departamentos;"
            cursor.execute(sql)
            departamentos = cursor.fetchall()
            if departamentos:
                for departamento in departamentos:
                    print(f"ID: {departamento[0]}, Nombre: {departamento[1]}, ID Gerente: {departamento[2]}")
            else:
                print("No se encontraron departamentos en la base de datos.")
        except ValueError as a:
            print(f"Error al mostrar departamentos: {a}")
        finally:
            cursor.close()

    def asignar_gerente_a_departamento(self, id_departamento: int, id_gerente: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql_departamento = "SELECT 1 FROM departamentos WHERE id_departamentos = %s;"
            cursor.execute(sql_departamento, (id_departamento,))
            departamento_valido = cursor.fetchone()
            sql_empleado = "SELECT 1 FROM empleados WHERE id_empleado = %s;"
            cursor.execute(sql_empleado, (id_gerente,))
            empleado_valido = cursor.fetchone()
            if departamento_valido and empleado_valido:
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
                if not departamento_valido:
                    print(f"No se encontró el departamento con ID: {id_departamento}.")
                if not empleado_valido:
                    print(f"No se encontró el empleado con ID {id_gerente}.")
                return False
        except ValueError as a:
            print(f"Error al asignar gerente al departamento: {a}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_departamentos_con_gerente(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """SELECT d.id_departamentos, d.nombre_departamento, e.nombre_empleado AS nombre_gerente
                    FROM departamentos d
                    LEFT JOIN empleados e ON d.id_gerente = e.id_empleado;"""
            cursor.execute(sql)
            departamentos = cursor.fetchall()  # Obtener todos los resultados
            return departamentos
        except ValueError as a:
            print(f"Error al mostrar departamentos con gerentes: {a}")
            return None
        finally:
            cursor.close()

    def obtener_departamentos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "SELECT id_departamentos, nombre_departamento FROM departamentos;"
            cursor.execute(sql)
            departamentos = cursor.fetchall()
            cursor.close()
            return departamentos
        except ValueError as a:
            print(f"Error al obtener departamentos: {a}")
            return []

    def insertar_departamento(self, nombre_departamento, id_gerente):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """INSERT INTO departamentos (nombre_departamento, id_gerente)
                    VALUES (%s, %s);"""
            cursor.execute(sql, (nombre_departamento, id_gerente))
            cnx.commit()
            cursor.close()
            return True
        except ValueError as a:
            print(f"Error al insertar departamento: {a}")
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
        except ValueError as a:
            print(f"Error al actualizar departamento: {a}")
            cnx.rollback()
            return False
