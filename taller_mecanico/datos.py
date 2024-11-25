# pip install mysql-connector-python==8.3.0
# cd Downloads\taller_mecanico
# c:\xampp\mysql\bin\mysql -u root < db\script_taller_mecanico.sql
# c:\xampp\mysql\bin\mysql -u root < db\dml_mecanico.sql
# c:\xampp\mysql\bin\mysql -u root < db\script_usuario.sql

from mysql.connector import MySQLConnection, connect
from modelo import Mecanico, Cliente, Vehiculo, Usuario
import hashlib

class Clave:
    def cifrar(texto_raw:str) -> str:
        text_codificado = texto_raw.encode()
        hash = hashlib.md5(text_codificado).hexdigest()
        return hash

class CrudUsuario:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'taller_mecanico'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx
    
    def registrar(self, usuario:Usuario) -> Usuario|None:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "insert into usuario values(%s, %s, %s)"
            hash = Clave.cifrar(usuario.clave)
            val = (usuario.nombre, hash, usuario.es_admin)
            cursor.execute(sql, val)
            cnx.commit()
            if cursor.rowcount > 0:
                return usuario
            else:
                return None
        except Exception as ex:
            raise Exception("Error en registro: ", ex)
        finally:
            cursor.close()
            cnx.close()

    def login(self, nombre:str, clave:str) -> Usuario|None:
        try:
            cnx = self.conectar()
            cursor = cnx.cursor()
            sql = "select * from usuario where nombre_usuario=%s"
            val = (nombre,)
            cursor.execute(sql, val)
            row = cursor.fetchone()
            if row is not None:
                hash = Clave.cifrar(clave)
                usuario = Usuario(nombre=row[0], clave=row[1], es_admin=row[2])
                if usuario.clave == hash:
                    return usuario
            else:
                return None
        except Exception as ex:
            raise Exception("Error de inicio de sesion: ", ex)
        finally:
            cursor.close()
            cnx.close()

class CrudMecanico:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'taller_mecanico'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx
    
    def insertar(self, mecanico:Mecanico) -> bool:
        # Obtener una conexion
        cnx = self.conectar()
        # Crear un cursor
        cursor = cnx.cursor()
        # Configurar la consulta con parametros
        sql = 'insert into persona(nombre, apellido) values (%s, %s)'
        # Tupla con parametros
        values = (mecanico.nombre, mecanico.apellido)
        # Ejecutar la consulta + los parametros
        cursor.execute(sql, values)
        # Obtener el id insertado en la tabla persona
        id_persona = cursor.lastrowid
        sql2 = 'insert into mecanico(valor_honorario, id_persona) values (%s, %s)'
        values2 = (mecanico.honorario, id_persona)
        cursor.execute(sql2, values2)
        cnx.commit()
        cursor.close()
        cnx.close()
        return
    
    def obtener(self) -> list[Mecanico]:
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql = 'select nombre, apellido, valor_honorario from persona, mecanico '
        sql += 'where persona.id_persona = mecanico.id_persona'
        cursor.execute(sql)
        # resultset es una lista de tuplas, cada item de la tupla representa un valor de columna
        resultset = cursor.fetchall()
        mecanicos = []
        for row in resultset:
            mec = Mecanico(nombre=row[0], apellido=row[1], honorario=row[2])
            mecanicos.append(mec)
        cursor.close()
        cnx.close()
        return mecanicos

    def modificar(self, mecanico:Mecanico, nuevo_honorario:int) -> bool:
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql = 'select id_persona from persona where nombre=%s and apellido=%s'
        values = (mecanico.nombre, mecanico.apellido)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result is not None:
            id_persona = result[0]
            sql2 = 'update mecanico set valor_honorario=%s where id_persona=%s'
            values2 = (nuevo_honorario, id_persona)
            cursor.execute(sql2, values2)
            cnx.commit()
        cursor.close()
        cnx.close()
        return True

    def eliminar(self, mecanico:Mecanico) -> bool:
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql = 'select id_persona from persona where nombre=%s and apellido=%s'
        values = (mecanico.nombre, mecanico.apellido)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        if result is not None:
            id_persona = result[0]
            sql2 = 'delete from mecanico where id_persona=%s;'
            values2 = (id_persona, )
            cursor.execute(sql2, values2)
            sql3 = 'delete from persona where id_persona=%s'
            values3 = (id_persona, )
            cursor.execute(sql3, values3)
            cnx.commit()
        cursor.close()
        cnx.close()
        return True

class CrudCliente:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'taller_mecanico'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def obtener(self) -> list[Cliente]|None:
        cnx = self.conectar()
        cursor = cnx.cursor()
        query = "select nombre, apellido, telefono from persona join cliente using(id_persona)"
        cursor.execute(query)
        result = cursor.fetchall()
        clientes = []
        for row in result:
            cli = Cliente(nombre=row[0], apellido=row[1], telefono=row[2])
            clientes.append(cli)
        cursor.close()
        cnx.close()
        return clientes

    def buscar(self, nombre:str, apellido:str) -> Cliente|None:
        cnx = self.conectar()
        cursor = cnx.cursor()
        query = "select nombre, apellido, telefono from persona join cliente where persona.id_persona = cliente.id_persona and nombre=%s and apellido=%s"
        values = (nombre, apellido)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None:
            cliente = Cliente(nombre=result[0], apellido=result[1], telefono=result[2])
            cursor.close()
            cnx.close()
            return cliente
        return None
    
    def buscar_id(self, id_cliente:int) -> Cliente|None:
        cnx = self.conectar()
        cursor = cnx.cursor()
        query = 'select nombre, apellido, telefono from persona join cliente where persona.id_persona = cliente.id_persona and cliente.id_cliente = %s'
        values = (id_cliente,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is not None:
            cliente = Cliente(nombre=result[0], apellido=result[1], telefono=result[2])
            cursor.close()
            cnx.close()
            return cliente
        return None

class CrudVehiculo:
    def __init__(self) -> None:
        self.username = 'root'
        self.password = ''
        self.database = 'taller_mecanico'

    def conectar(self) -> MySQLConnection:
        cnx = connect(user=self.username, password=self.password, database=self.database)
        return cnx

    def obtener(self) -> list[Vehiculo]:
        cnx = self.conectar()
        cursor = cnx.cursor()
        query = 'select patente_vehiculo, marca, modelo, agno, id_cliente from vehiculo'
        cursor.execute(query)
        result = cursor.fetchall()
        vehiculos:list[Vehiculo] = []
        for row in result:
            vehiculo = Vehiculo(patente=row[0], marca=row[1], modelo=row[2], año=row[3], dueño=CrudCliente().buscar_id(row[4]))
            vehiculos.append(vehiculo)
        cursor.close()
        cnx.close()
        return vehiculos

    def ingresar(self, vehiculo:Vehiculo) -> bool:
        cnx = self.conectar()
        cursor = cnx.cursor()
        sql = "select id_cliente from persona join cliente using(id_persona) where nombre=%s and apellido=%s"
        val = (vehiculo.dueño.nombre, vehiculo.dueño.apellido)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is not None:
            id_cliente = int(result[0])
            query = 'insert into vehiculo(patente_vehiculo, marca, modelo, agno, id_cliente) values (%s, %s, %s, %s, %s)'
            values = (vehiculo.patente, vehiculo.marca, vehiculo.modelo, vehiculo.año, id_cliente)
            cursor.execute(query, values)
            cnx.commit()
            cursor.close()
            cnx.close()
            return True
        return False