import requests

BASE_URL = "https://mindicador.cl/api/"

class MiIndicador:

    def fetch_indicador(self, indicador:str, fecha:str):
        try:
            url = f"https://mindicador.cl/api/{indicador}/{fecha}"
            self.datos_indicador = requests.get(url)
            if self.datos_indicador.status_code == 200:
                return self.datos_indicador.json(), url
            else:
                raise ValueError("Error en la solicitud a la API.")
        except Exception as e:
            print(f"Error: {e}")
            return None
            
#TEST
#ind = MiIndicador()
#print(ind.fetch_indicador("uf", "10-11-2024"))