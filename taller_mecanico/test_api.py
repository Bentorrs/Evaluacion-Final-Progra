#pip install requests
import requests, json

BASE_URL = "http://localhost/api/taller_mecanico.php"

def registrar_usuario(nombre_usuario, clave, es_admin):
    url = f"{BASE_URL}?action=register"
    data = {"nombre_usuario": nombre_usuario, "clave": clave, "es_admin": es_admin}
    response = requests.post(url, json=data)
    #print("Status Code:", response.status_code)
    #print("Response Content:", response.text)
    if response.status_code == 200:
        json_text = response.text
        # deserializar JSON a un diccionario de Python
        json_dict = json.loads(json_text)
        print(json_dict["message"])
    try:
        print("Registro:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Error: La respuesta no es un JSON válido")

def iniciar_sesion(nombre_usuario, clave):
    url = f"{BASE_URL}?action=login"
    data = {"nombre_usuario": nombre_usuario, "clave": clave}
    response = requests.post(url, json=data)
    #print("Status Code:", response.status_code)
    #print("Response Content:", response.text)
    if response.status_code == 200:
        json_text = response.text
        # deserializar JSON a un diccionario de Python
        json_dict = json.loads(json_text)
        print(json_dict["message"])
        print(json_dict["nombre_usuario"])
        if json_dict["es_admin"] == 1:
            print("Es administrador")
        else:
            print("Es un usuario normal")
    try:
        print("Registro:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Error: La respuesta no es un JSON válido")

if __name__ == "__main__":

    print("\nProbando inicio de sesión con usuario admin:")
    iniciar_sesion("admin", "admin")

    #print("Probando registro de usuario:")
    #registrar_usuario("anita", "123", 0)

    print("\nProbando inicio de sesión:")
    iniciar_sesion("anita", "123")