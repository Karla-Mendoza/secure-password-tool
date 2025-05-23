import re
import base64
import hashlib
import random
import string

# Función para validar contraseñas
def validar_contrasena(contrasena):
    # Define los criterios de validación
    longitud_minima = 12
    contiene_mayuscula = any(c.isupper() for c in contrasena)
    contiene_minuscula = any(c.islower() for c in contrasena)
    contiene_numero = any(c.isdigit() for c in contrasena)
    contiene_caracter_especial = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", contrasena))

    # Verifica todos los criterios
    if len(contrasena) < longitud_minima:
        return "La contraseña debe tener al menos 12 caracteres."
    if not contiene_mayuscula:
        return "La contraseña debe contener al menos una letra mayúscula."
    if not contiene_minuscula:
        return "La contraseña debe contener al menos una letra minúscula."
    if not contiene_numero:
        return "La contraseña debe contener al menos un número."
    if not contiene_caracter_especial:
        return "La contraseña debe contener al menos un carácter especial."

    return "Contraseña válida."

# Función para generar contraseñas seguras
def generar_contrasena():
    longitud = 12
    caracteres = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*(),.?\":{}|<>"
    )
    while True:
        contrasena = ''.join(random.choice(caracteres) for _ in range(longitud))
        if validar_contrasena(contrasena) == "Contraseña válida.":
            return contrasena

# Generar clave simple usando hashing
def generar_clave():
    clave = base64.urlsafe_b64encode(hashlib.sha256(b"mi_clave_secreta").digest())
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)
    print("Clave generada y guardada en 'clave.key'")

# Cargar clave desde un archivo
def cargar_clave():
    try:
        with open("clave.key", "rb") as archivo_clave:
            return archivo_clave.read()
    except FileNotFoundError:
        print("No se encontró 'clave.key'. Genera una clave primero.")
        return None

# Encriptar contraseña utilizando una clave y base64
def encriptar_contrasena(contrasena, clave):
    clave_hash = hashlib.sha256(clave).digest()
    contrasena_bytes = contrasena.encode()
    contrasena_encriptada = base64.b64encode(contrasena_bytes + clave_hash[:16])
    return contrasena_encriptada

# Desencriptar contraseña utilizando una clave y base64
def desencriptar_contrasena(contrasena_encriptada, clave):
    clave_hash = hashlib.sha256(clave).digest()
    contrasena_bytes = base64.b64decode(contrasena_encriptada)
    contrasena_original = contrasena_bytes[:-16].decode()
    return contrasena_original

# Menú principal
def menu():
    while True:
        print("\n** Validador y Gestor de Contraseñas **")
        print("1. Validar contraseña")
        print("2. Generar contraseña segura")
        print("3. Generar clave de encriptación")
        print("4. Encriptar contraseña")
        print("5. Desencriptar contraseña")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            contrasena = input("Ingresa la contraseña que deseas validar: ")
            resultado = validar_contrasena(contrasena)
            print(resultado)
        elif opcion == "2":
            contrasena_segura = generar_contrasena()
            print("Contraseña segura generada:", contrasena_segura)
        elif opcion == "3":
            generar_clave()
        elif opcion == "4":
            clave = cargar_clave()
            if clave:
                contrasena = input("Ingresa la contraseña que deseas encriptar: ")
                contrasena_encriptada = encriptar_contrasena(contrasena, clave)
                print("Contraseña encriptada:", contrasena_encriptada.decode())
        elif opcion == "5":
            clave = cargar_clave()
            if clave:
                contrasena_encriptada = input("Ingresa la contraseña encriptada: ").encode()
                try:
                    contrasena_desencriptada = desencriptar_contrasena(contrasena_encriptada, clave)
                    print("Contraseña desencriptada:", contrasena_desencriptada)
                except Exception as e:
                    print("Error al desencriptar la contraseña:", e)
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()