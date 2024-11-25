import mysql.connector
from datetime import datetime
from modelo import Empleado

import mysql.connector
from mysql.connector import Error

class crud_empleado:
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
    
    def insertar(self, empleado):
        try:
            cursor = self.cnx.cursor() 
            sql = """INSERT INTO empleados (nombre, direccion, telefono, correo, fecha_contrato, salario, nombre_departamento)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            valores = (empleado.nombre, empleado.direccion, empleado.telefono, empleado.correo,
                    empleado.fecha_contrato, empleado.salario, empleado.nombre_departamento)
            cursor.execute(sql, valores)
            self.cnx.commit() 
            print("Empleado ingresado exitosamente")
        except Error as e:
            print(f"Error al insertar empleado: {e}")
            if cursor:
                self.cnx.rollback()
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_empleado: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """SELECT * FROM empleados 
                    WHERE id_empleado = %s;"""
            cursor.execute(sql, (id_empleado,))
            empleado = cursor.fetchone()
            if empleado:
                print(f"""Empleado encontrado: ID: {empleado[0]}, Nombre: {empleado[1]},
                    Dirección: {empleado[2]}, Teléfono: {empleado[3]},
                    Correo: {empleado[4]},Fecha Contrato: {empleado[5]},
                    Salario: {empleado[6]}, ID Departamento: {empleado[7]}""")
                return empleado
            else:
                print("No se encontró el empleado con ID {}.".format(id_empleado))
                return None
        except ValueError:
            print("Error al buscar empleado por ID")
        finally:
            cursor.close()

    def mostrar_todos(self):
            try:
                cnx = self.conectar()
                cursor = cnx.cursor()
                query = "SELECT * FROM empleados;"
                cursor.execute(query)
                empleados = cursor.fetchall()
                if empleados:
                    for empleado in empleados:
                        print(f"""ID: {empleado[0]}, Nombre: {empleado[1]}, Dirección: {empleado[2]}, 
                        Teléfono: {empleado[3]}, Correo: {empleado[4]},
                        Fecha Contrato: {empleado[5]}, Salario: {empleado[6]}, ID Departamento: {empleado[7]}""")
                else:
                    print("No se encontraron empleados en la base de datos.")
            except ValueError:
                print("Error al mostrar empleados")
            finally:
                cursor.close()

    def modificar(self, id_empleado: int, nuevo_nombre: str, nueva_direccion: str, nuevo_telefono: str, 
                nuevo_correo: str, nueva_fecha_contrato: datetime, nuevo_salario: int, nuevo_id_departamento: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_comp = "SELECT 1 FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_comp, (id_empleado,))
            if cursor.fetchone():
                query_mod = """
                UPDATE empleados SET nombre = %s, direccion = %s, telefono = %s, 
                correo = %s, fecha_contrato = %s, 
                salario = %s, Departamento_id_departamento = %s 
                WHERE id_empleado = %s;
                """
                values = (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_correo, nueva_fecha_contrato, 
                        nuevo_salario, nuevo_id_departamento, id_empleado)
                cursor.execute(query_mod, values)
                cnx.commit()
                print("Empleado actualizado correctamente.")
                return True
            else:
                print("No se encontró el empleado con ID {}.".format(id_empleado))
                return False
        except ValueError:
            print("Error al modificar empleado: {}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def eliminar(self, empleado_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_nombre_usuario = "SELECT autentificador_nombre_usuario FROM empleados WHERE id_empleado = %s;"
            cursor.execute(query_nombre_usuario, (empleado_id,))
            resultado = cursor.fetchone()
            if not resultado:
                print("Error: No se encontró el empleado.")
                return False
            nombre_usuario = resultado[0]
            query_eliminar_empleado = "DELETE FROM empleados WHERE id_empleado = %s;"
            cursor.execute(query_eliminar_empleado, (empleado_id,))
            query_eliminar_autentificador = "DELETE FROM autentificador WHERE nombre_usuario = %s;"
            cursor.execute(query_eliminar_autentificador, (nombre_usuario,))
            cnx.commit()
            cursor.close()
            return True
        except ValueError:
            print("Error al eliminar empleado")
            cnx.rollback()
            return False

    def obtener(self) -> list[Empleado]:
        try:
            cnx = self.cnx
            cursor = cnx.cursor()
            sql = """SELECT id_empleado, nombre, direccion, numero, correo,
                    fecha_contrato, salario, DEPARTAMENTO_id_departamento,
                    FROM empleado;"""
            cursor.execute(sql)
            result = cursor.fetchall()
            empleados: list[Empleado] = []
            for row in result:
                empleado = Empleado(
                    nombre=row[1],
                    direccion=row[2],
                    telefono=row[3],
                    correo=row[4],
                    fecha_contrato=row[5],
                    salario=row[6],
                    DEPARTAMENTO_id_departamento=row[7]
                )
                empleado.id_empleado = row[0]
                empleados.append(empleado)
            cursor.close()
            cnx.close()
            return empleados
        except ValueError:
            print("Error al obtener empleados")
            return []

    def obtener_todos(self):
        try:
            cnx = self.cnx
            cursor = cnx.cursor()
            query = "SELECT id_empleado, nombre_empleado FROM empleados;"
            cursor.execute(query)
            empleados = cursor.fetchall()
            cursor.close()
            return empleados
        except ValueError:
            print("Error al obtener empleados")
            return []

    def actualizar(self, id_empleado: int, campos: dict):
        try:
            set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
            query = f"UPDATE empleados SET {set_clause} WHERE id_empleado = %s"
            values = list(campos.values())
            values.append(id_empleado)
            cnx = self.cnx
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            cnx.rollback()
            return False

    def actualizar_empleado(self, id_empleado: int, campos: dict):
        if not campos:
            return True
        try:
            set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
            query = f"UPDATE empleados SET {set_clause} WHERE id_empleado = %s"
            values = list(campos.values()) + [id_empleado]
            cnx = self.conectar()
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar empleado: {e}")
            cnx.rollback()
            return False

    def eliminar_empleado(self, empleado_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_autentificador = "SELECT autentificador_nombre_usuario FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_autentificador, (empleado_id,))
            resultado = cursor.fetchone()
            if resultado:
                nombre_usuario = resultado[0]
            else:
                print("No se encontró un autentificador asociado para este empleado.")
                return False
            query_eliminar_empleado = "DELETE FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_eliminar_empleado, (empleado_id,))
            query_eliminar_autentificador = "DELETE FROM autentificador WHERE nombre_usuario = %s"
            cursor.execute(query_eliminar_autentificador, (nombre_usuario,))
            cnx.commit()
            cursor.close()
            return True
        except ValueError as a:
            print(f"Error al eliminar empleado y autentificador: {a}")
            cnx.rollback() 
            return False

    def obtener_empleados_por_departamento(self, departamento_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """
            SELECT id_empleado, nombre, salario
            FROM empleados
            WHERE DEPARTAMENTO_id_departamento = %s
            """
            cursor.execute(sql, (departamento_id,))
            empleados = cursor.fetchall()
            return empleados
        except ValueError as a:
            print(f"Error al obtener empleados por departamento: {a}")
            return []
        finally:
            cursor.close()

