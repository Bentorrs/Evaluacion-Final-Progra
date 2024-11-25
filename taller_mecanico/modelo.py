from datetime import datetime

class Usuario:
    def __init__(self, nombre:str, clave:str, es_admin:bool) -> None:
        self.nombre = nombre
        self.clave = clave
        self.es_admin = es_admin

class Persona:
    # constructor con dos argumentos
    def __init__(self, nombre:str, apellido:str) -> None:
        self.nombre = nombre
        self.apellido = apellido

    # self representar la instancia actual de la clase
    def imprimir(self):
        print(self.nombre, self.apellido)

class Cliente(Persona):
    def __init__(self, nombre:str, apellido:str, telefono:str) -> None:
        super().__init__(nombre, apellido)
        self.telefono = telefono

class Mecanico(Persona):
    def __init__(self, nombre: str, apellido: str, honorario:int) -> None:
        super().__init__(nombre, apellido)
        self.honorario = honorario

class Vehiculo:
    def __init__(self, patente:str, marca:str, modelo:str, año:int, dueño:Cliente) -> None:
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.dueño = dueño

class Repuesto:
    def __init__(self, num_serie:str, marca:str, costo:int) -> None:
        self.num_serie = num_serie
        self.marca = marca
        self.costo = costo

from datetime import datetime

class Trabajo:
    def __init__(self, fecha_ingreso:datetime, estado_inicial:str, vehiculo:Vehiculo) -> None:
        self.fecha_ingreso = fecha_ingreso
        self.fecha_entrega = None
        self.estado_inicial = estado_inicial
        self.reparaciones = str()
        self.vehiculo = vehiculo
        self.lista_mecanicos:list[Mecanico] = []
        self.lista_repuestos:list[Repuesto] = []

    # agregacion con mecanico
    def agregar_mecanico(self, mecanico:Mecanico):
        self.lista_mecanicos.append(mecanico)
    
    # composicion con repuesto
    def componer_repuesto(self, num_serie:str, marca:str, costo:int):
        repuesto = Repuesto(num_serie, marca, costo)
        self.lista_repuestos.append(repuesto)

    def obtener_precio_total(self) -> int:
        costo_honorarios = 0
        costo_repuestos = 0
        for mec in self.lista_mecanicos:
            costo_honorarios = costo_honorarios + mec.honorario
        for rep in self.lista_repuestos:
            costo_repuestos = costo_repuestos + rep.costo
        costo_total = (costo_honorarios + costo_repuestos) * 1.23
        return round(costo_total)
