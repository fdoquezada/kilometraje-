import secrets

def generar_secret_key(longitud=50):
    return secrets.token_urlsafe(longitud)

if __name__ == "__main__":
    clave = generar_secret_key()
    print(f"SECRET_KEY = '{clave}'")
