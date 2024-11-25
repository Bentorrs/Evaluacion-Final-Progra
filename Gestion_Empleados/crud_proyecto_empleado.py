import mysql.connector

class crud_proyecto_empleado:
    def conectar() -> mysql.connector.MySQLConnection:
        cnx = mysql.connector.connect(
            username='root',
            password='',
            database='gestion_empleados')
        return cnx
    
    def asignar_empleado_proyecto(self, id_proyecto:int, id_empleado:int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """INSERT INTO proyecto_has_empleado (proyecto_id_proyecto, id_empleado)
                    VALUES (%s, %s);"""
            cursor.execute(sql, (id_proyecto, id_empleado))
            return True
        except:
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()
        
    def visualizar_asignaciones(self):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """SELECT p.id_proyecto, p.nombre_proyecto, e.id_empleado, e.nombre_empleado 
                    FROM proyectos_has_empleados proemp
                    JOIN proyectos p ON proemp.proyectos_id_proyectos = p.id_proyectos
                    JOIN empleados e ON proemp.id_empleado = e.id_empleado;"""
            cursor.execute(sql)
            asignaciones = cursor.fetchall()
            if asignaciones:
                for asignacion in asignaciones:
                    print(f"""ID Proyecto: {asignacion[0]}, Nombre Proyecto: {asignacion[1]},
                           ID Empleado: {asignacion[2]}, Nombre Empleado: {asignacion[3]}""")
            else:
                print("Asignaciones de empleados a proyectos no encontrados.")
        except:
            print("Error")
        finally:
            cursor.close()

    def visualizar_asignaciones_proyecto(self, id_proyecto: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """SELECT p.id_proyecto, p.nombre_proyecto, e.id_empleado, e.nombre_empleado 
                    FROM proyecto_has_empleado proemp
                    JOIN proyecto p ON proemp.proyecto_id_proyecto = p.id_proyecto
                    JOIN empleado e ON proemp.id_empleado = e.id_empleado
                    WHERE p.id_proyecto = %s;"""
            cursor.execute(sql, (id_proyecto,))
            asignaciones = cursor.fetchall()
            if asignaciones:
                for asignacion in asignaciones:
                    print(f"""ID Proyecto: {asignacion[0]}, Nombre Proyecto: {asignacion[1]},
                           ID Empleado: {asignacion[2]}, Nombre Empleado: {asignacion[3]}""")
            else:
                print(f"No existen asignaciones con ID: {id_proyecto}.")
        except:
            print("Error")
        finally:
            cursor.close()
    
    def visualizar_proyectos_empleado(self, id_empleado: int):
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = """SELECT p.id_proyecto, p.nombre_proyecto, p.descripcion_proyecto 
                    FROM proyecto_has_empleado proemp
                    JOIN proyecto p ON proemp.proyecto_id_proyecto = p.id_proyecto
                    WHERE proemp.id_empleado = %s;"""
            cursor.execute(sql, (id_empleado,))
            proyectos = cursor.fetchall()
            if proyectos:
                print("Proyectos asociados al empleado con ID {}:".format(id_empleado))
                for proyecto in proyectos:
                    print(f"ID Proyecto: {proyecto[0]}, Nombre Proyecto: {proyecto[1]}, Descripción: {proyecto[2]}")
            else:
                print(f"No existen proyectos enlazados con el ID: {id_empleado}.")
        except:
            print("Error")
        finally:
            cursor.close()

    def eliminar_asignacion(self, id_proyecto: int, id_empleado: int) -> bool:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql1 = """SELECT 1 FROM proyectos_has_empleados
                    WHERE proyecto_id_proyecto = %s AND id_empleado = %s;"""
            cursor.execute(sql1, (id_proyecto, id_empleado))
            asignacion_valida = cursor.fetchone()
            if not asignacion_valida:
                print(f"No se existe una asignación para el proyecto con el ID proyecto: {id_proyecto} y con el ID empleado: {id_empleado}.")
                return False
            eliminar_sql = """DELETE FROM proyectos_has_empleados 
                            WHERE proyecto_id_proyecto = %s AND id_empleado = %s;"""
            cursor.execute(eliminar_sql, (id_proyecto, id_empleado))
            cnx.commit()
            return True
        except:
            print("Error")
            if cnx.is_connected():
                cnx.rollback()
            return False
        finally:
            cursor.close()