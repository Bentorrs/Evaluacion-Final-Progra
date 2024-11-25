import hashlib

class Clave:
    def cifrar(texto_raw:str) -> str:
        text_codificado = texto_raw.encode('utf-8')
        hash = hashlib.md5(text_codificado).hexdigest()
        return hash

contraseña = "test"
hash = Clave.cifrar(contraseña)
print(hash)