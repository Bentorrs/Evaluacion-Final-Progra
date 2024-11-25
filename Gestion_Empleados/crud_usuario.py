import mysql.connector

class crud_usuario:
    def conectar() -> mysql.connector.MySQLConnection:
        cnx = mysql.connector.connect(
            username='root',
            password='',
            database='gestion_empleados')
        return cnx
    
    def insertar_usuario(nombre_usuario:str, contraseña:str) -> bool:
        cnx = crud_usuario.conectar()
        cursor = cnx.cursor()
        insert = 'INSERT INTO usuario(nombre_usuario, contraseña) VALUES (%s, %s)'
        values = (nombre_usuario, contraseña)
        cursor.execute(insert, values)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    
    def obtener_usuarios() -> None:
        cnx = crud_usuario.conectar()
        cursor = cnx.cursor()
        select = 'SELECT id_usuario, nombre_usuario FROM usuario'
        cursor.execute(select)
        resultset = cursor.fetchall()
        for row in resultset:
            print(f'ID: {row[0]}, Nombre de Usuario: {row[1]}')
        cursor.close()
        cnx.close()
        return
    
    def modificar_usuario(id_usuario:int, nombre_usuario:str, contraseña:str) -> bool:
        cnx = crud_usuario.conectar()
        cursor = cnx.cursor()
        update = 'UPDATE usuario SET nombre_usuario=%s, contraseña=%s WHERE id_usuario=%s'
        values = (nombre_usuario, contraseña, id_usuario)
        cursor.execute(update, values)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    
    def eliminar_usuario(id_usuario:int) -> bool:
        cnx = crud_usuario.conectar()
        cursor = cnx.cursor()
        delete = 'DELETE FROM usuario WHERE id_usuario=%s'
        values = (id_usuario,)
        cursor.execute(delete, values)
        cnx.commit()
        cursor.close()
        cnx.close()
        return True