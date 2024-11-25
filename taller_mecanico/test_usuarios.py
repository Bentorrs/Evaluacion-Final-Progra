from datos import CrudUsuario
from modelo import Usuario

try:
    if CrudUsuario().login("pedrito", "falsa") is not None:
        print("Inicio de sesion exitoso!")
except Exception as ex:
    print(ex)