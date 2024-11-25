from mysql.connector import MySQLConnection, connect, Error
from datetime import datetime
from Modelo_Final import Empleado, Usuario
from API_INDICE import MiIndicador
import hashlib

class Clave:
    def cifrar(texto_raw:str) -> str:
        text_codificado = texto_raw.encode('utf-8')
        hash = hashlib.md5(text_codificado).hexdigest()
        return hash
    
class CRUDempleado:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'ecotechsoluciones'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def insertar(self, empleado) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM usuario WHERE nombre_usuario = %s" 
            cursor.execute(query_check, (empleado.nombre_usuario,))
            usuario_existe = cursor.fetchone()

            if usuario_existe:
                print("El nombre de usuario '{}' ya existe. No se puede insertar el empleado.".format(empleado.nombre_usuario))
                return False

            query1 = "INSERT INTO usuario (nombre_usuario, contrasenna, es_admin) VALUES (%s, %s, %s);"
            values1 = (empleado.nombre_usuario, empleado.contrasenna, empleado.es_admin)
            cursor.execute(query1, values1)

            query2 = """
            INSERT INTO empleados (nombre_empleado, direccion_empleado, numero_telefono, correo_electronico_empleado, 
                                fecha_inicio_contrato, salario_empleado, departamentos_id_departamentos, 
                                usuario_nombre_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            values2 = (
                empleado.nombre_empleado, empleado.direccion_empleado, empleado.numero_telefono, 
                empleado.correo_electronico_empleado, empleado.fecha_inicio_contrato, empleado.salario_empleado, 
                empleado.departamentos_id_departamentos, empleado.nombre_usuario
            )
            cursor.execute(query2, values2)
            
            cnx.commit()
            print("Empleado insertado correctamente en ambas tablas.")
            return True
        except Error as e:
            print(f"Error al insertar empleado: {e}")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def iniciar_sesion(self, usuario:str, contraseña:str, rol:str):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql_query = "SELECT nombre_usuario, contrasenna, es_admin FROM usuario WHERE nombre_usuario = %s"
            cursor.execute(sql_query, (usuario,))
            resultado = cursor.fetchone()
            hash_contraseña = Clave.cifrar(contraseña)
            usuario_db = Usuario(nombre_usuario=resultado[0], contrasenna=resultado[1], es_admin=resultado[2])
            if usuario_db.contrasenna == hash_contraseña:
                if rol == "Administrador" and usuario_db.es_admin == 1:
                    return "admin"
                elif rol == "Usuario" and usuario_db.es_admin == 0:
                    return "usuario"
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"Error en la conexion: {e}")

    def registro_informacion(self, indicador:str, usuario:str, fecha:str, url:str):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql_query = """INSERT INTO datos_economicos (nombre_indicador, fecha, fecha_consulta, 
                            usuario_nombre_usuario, sitio_origen)
                            VALUES (%s, %s, SYSDATE(), %s, %s)"""
            values = (indicador, fecha, usuario, url)
            cursor.execute(sql_query, values)
            cnx.commit()
            return True
        except KeyError:
            print("Error para registrar los datos.")

    def existe_empleado(self, id_usuario):
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql_query = "SELECT * FROM empleado WHERE nombre_usuario = %s"
        cursor.execute(sql_query, (id_usuario,))
        resultado = cursor.fetchone()
        cursor.close()
        cnx.close()
        return resultado is not None
    
    def buscar_por_id(self, id_empleado: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            SELECT * FROM empleados 
            WHERE id_empleado = %s;
            """
            cursor.execute(query, (id_empleado,))
            empleado = cursor.fetchone()
            if empleado:
                print("Empleado encontrado: ID: {}, Nombre: {}, Dirección: {}, Teléfono: {}, Correo: {}, "
                    "Fecha Contrato: {}, Salario: {}, ID Departamento: {}, Nombre Usuario: {}".format(
                    empleado[0], empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], 
                    empleado[6], empleado[7], empleado[8]))
                return empleado
            else:
                print("No se encontró el empleado con ID {}.".format(id_empleado))
                return None
        except Error as e:
            print("Error al buscar empleado por ID: {}".format(e))
        finally:
            cursor.close()

    def buscar_por_nombre_usuario(self, nombre_usuario: str):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            SELECT * FROM empleados 
            WHERE usuario_nombre_usuario = %s;
            """
            cursor.execute(query, (nombre_usuario,))
            empleado = cursor.fetchone()
            if empleado:
                print("Empleado encontrado: ID: {}, Nombre: {}, Dirección: {}, Teléfono: {}, Correo: {}, "
                    "Fecha Contrato: {}, Salario: {}, ID Departamento: {}, Nombre Usuario: {}".format(
                    empleado[0], empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], 
                    empleado[6], empleado[7], empleado[8]))
                return empleado
            else:
                print("No se encontró el empleado con el nombre de usuario '{}'.".format(nombre_usuario))
                return None
        except Error as e:
            print("Error al buscar empleado por nombre de usuario: {}".format(e))
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
                        print("ID: {}, Nombre: {}, Dirección: {}, Teléfono: {}, Correo: {}, Fecha Contrato: {}, "
                            "Salario: {}, ID Departamento: {}, Nombre Usuario: {}".format(
                            empleado[0], empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], 
                            empleado[6], empleado[7], empleado[8]))
                else:
                    print("No se encontraron empleados en la base de datos.")
            except Error as e:
                print("Error al mostrar empleados: {}".format(e))
            finally:
                cursor.close()

    def modificar(self, id_empleado: int, nuevo_nombre: str, nueva_direccion: str, nuevo_telefono: str, 
                nuevo_correo: str, nueva_fecha_inicio: datetime, nuevo_salario: int, nuevo_id_departamento: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_check = "SELECT 1 FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_check, (id_empleado,))
            if cursor.fetchone():
                query_update = """
                UPDATE empleados SET nombre_empleado = %s, direccion_empleado = %s, numero_telefono = %s, 
                                    correo_electronico_empleado = %s, fecha_inicio_contrato = %s, 
                                    salario_empleado = %s, departamentos_id_departamentos = %s 
                WHERE id_empleado = %s;
                """
                values = (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_correo, nueva_fecha_inicio, 
                        nuevo_salario, nuevo_id_departamento, id_empleado)
                cursor.execute(query_update, values)
                cnx.commit()
                print("Empleado actualizado correctamente.")
                return True
            else:
                print("No se encontró el empleado con ID {}.".format(id_empleado))
                return False
        except Error as e:
            print("Error al modificar empleado: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def eliminar(self, empleado_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_nombre_usuario = "SELECT usuario_nombre_usuario FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_nombre_usuario, (empleado_id,))
            resultado = cursor.fetchone()
            if not resultado:
                print("Error: No se encontró el empleado.")
                return False
            nombre_usuario = resultado[0]
            query_eliminar_empleado = "DELETE FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_eliminar_empleado, (empleado_id,))
            query_eliminar_usuario = "DELETE FROM usuario WHERE nombre_usuario = %s"
            cursor.execute(query_eliminar_usuario, (nombre_usuario,))
            cnx.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            cnx.rollback()
            return False

    def obtener(self) -> list[Empleado]:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            SELECT e.id_empleado, e.nombre_empleado, e.direccion_empleado, e.numero_telefono, e.correo_electronico_empleado,
                e.fecha_inicio_contrato, e.salario_empleado, e.departamentos_id_departamentos,
                a.nombre_usuario, a.contrasenna, a.es_admin
            FROM empleados e
            JOIN usuario a ON e.usuario_nombre_usuario = a.nombre_usuario;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            empleados: list[Empleado] = []
            for row in result:
                empleado = Empleado(
                    nombre_usuario=row[8],
                    contrasenna=row[9],
                    es_admin=row[10],
                    nombre_empleado=row[1],
                    direccion_empleado=row[2],
                    numero_telefono=row[3],
                    correo_electronico_empleado=row[4],
                    fecha_inicio_contrato=row[5],
                    salario_empleado=row[6],
                    departamentos_id_departamentos=row[7]
                )
                empleado.id_empleado = row[0]
                empleados.append(empleado)
            cursor.close()
            cnx.close()
            return empleados
        except Error as e:
            print("Error al obtener empleados: {}".format(e))
            return []

    def obtener_por_nombre(self, nombre_usuario):
        cnx = self.conectar()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombre_usuario,))
        usuario_data = cursor.fetchone()
        cursor.close()
        cnx.close()
        
        if usuario_data:
            # Crear un objeto Usuario con los datos obtenidos
            usuario = Usuario(
                nombre_usuario=usuario_data[0],  # El primer campo es nombre_usuario
                contrasenna=usuario_data[1],
                es_admin=usuario_data[2]
            )
            return usuario
        else:
            return None

    def obtener_todos(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = "SELECT id_empleado, nombre_empleado FROM empleados;"
            cursor.execute(query)
            empleados = cursor.fetchall()
            cursor.close()
            return empleados
        except Exception as e:
            print(f"Error al obtener empleados: {e}")
            return []
    
    def actualizar_contrasenna(self, nombre_usuario, nueva_contrasenna):
        cnx = self.conectar()
        cursor = cnx.cursor()
        query = "UPDATE usuario SET contrasenna = %s WHERE nombre_usuario = %s"
        cursor.execute(query, (nueva_contrasenna, nombre_usuario))
        cnx.commit()
        cursor.close()
        cnx.close()

    def actualizar(self, id_empleado: int, campos: dict):
        try:
            set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
            query = f"UPDATE empleados SET {set_clause} WHERE id_empleado = %s"
            values = list(campos.values())
            values.append(id_empleado)
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

    def actualizar_usuario(self, id_empleado: int, campos: dict):
        if not campos:
            return True
        try:
            set_clause = ", ".join([f"{campo} = %s" for campo in campos.keys()])
            query = f"""
                UPDATE usuario
                SET {set_clause}
                WHERE nombre_usuario = (
                    SELECT usuario_nombre_usuario FROM empleados WHERE id_empleado = %s
                );
            """
            values = list(campos.values()) + [id_empleado]
            cnx = self.conectar()
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
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
    
    def actualizar_empleado_ingresar(self, empleado):
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql_query = """
        UPDATE empleado
        SET nombre_empleado = %s, direccion_empleado = %s, numero_telefono = %s, 
            correo_electronico_empleado = %s, salario_empleado = %s, fecha_inicio_contrato = %s,
            departamentos_id_departamentos = %s
        WHERE nombre_usuario = %s
        """
        cursor.execute(sql_query, (
            empleado.nombre_empleado, 
            empleado.direccion_empleado,
            empleado.numero_telefono,
            empleado.correo_electronico_empleado,
            empleado.salario_empleado,
            empleado.fecha_inicio_contrato,
            empleado.departamentos_id_departamentos,
            empleado.nombre_usuario  # Usamos el id_usuario como identificador
        ))
        cnx.commit()
        cursor.close()
        cnx.close()
        return cursor.rowcount > 0  # Si se actualizó alguna fila, devuelve True

    def eliminar_empleado(self, empleado_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query_usuario = "SELECT usuario_nombre_usuario FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_usuario, (empleado_id,))
            resultado = cursor.fetchone()
            if resultado:
                nombre_usuario = resultado[0]
            else:
                print("No se encontró un usuario asociado para este empleado.")
                return False
            query_eliminar_empleado = "DELETE FROM empleados WHERE id_empleado = %s"
            cursor.execute(query_eliminar_empleado, (empleado_id,))
            query_eliminar_usuario = "DELETE FROM usuario WHERE nombre_usuario = %s"
            cursor.execute(query_eliminar_usuario, (nombre_usuario,))
            cnx.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error al eliminar empleado y usuario: {e}")
            cnx.rollback() 
            return False

    def obtener_empleados_por_departamento(self, departamento_id):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            query = """
            SELECT id_empleado, nombre_empleado, salario_empleado
            FROM empleados
            WHERE departamentos_id_departamentos = %s
            """
            cursor.execute(query, (departamento_id,))
            empleados = cursor.fetchall()
            return empleados
        except Error as e:
            print("Error al obtener empleados por departamento:", e)
            return []
        finally:
            cursor.close()

    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'ecotechsoluciones'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def asignar_empleado_a_proyecto(self, id_proyecto: int, id_empleado: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx.commit()
            print("Empleado asignado al proyecto correctamente.")
            return True
        except Error as e:
            print("Error al asignar empleado a proyecto: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()

    def mostrar_todas_asignaciones(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx = self.conectar()
            cursor = cnx.cursor()
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
            cnx.commit()
            print("Asignación eliminada correctamente.")
            return True
        except Error as e:
            print("Error al eliminar la asignación: {}".format(e))
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()
# # Nuevo = Empleado("psychotron", "ni idea", "Gerente", "Daniel Gutierrez", "Calle Falsa 56", "+56996102127", "kilo@example.org", 56000, 2008-1-10, 8)
# nuevo_2 = Empleado("tenuchito", "tenuchito:c", "Empleado", "Pedro Perez", "Calle Larga #216", "+569878562", "bbcto@example.org", 12000, datetime(2024,10,9),8)
# crud = CRUDempleado()
# crud.insertar(nuevo_2)

# crud.mostrar_todos()

# CRUDempleado().obtener()