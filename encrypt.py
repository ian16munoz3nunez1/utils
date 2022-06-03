import os
import sys
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def generarClave(clave):
    key = Fernet.generate_key()

    with open(clave, 'wb') as keyFile:
        keyFile.write(key)
    keyFile.close()

    print(Fore.GREEN + f"[+] Clave \"{clave}\" generada")

def cargarClave(clave):
    return open(clave, 'rb').read()

def encriptar(archivos, key):
    f = Fernet(key)
    for i in archivos:
        nombre = os.path.basename(i)
        with open(i, 'rb') as archivo:
            data = archivo.read()
        archivo.close()

        dataEncrypt = f.encrypt(data)

        with open(i, 'wb') as archivo:
            archivo.write(dataEncrypt)
        archivo.close()

        print(Fore.GREEN + f"[+] Archivo \"{nombre}\" encriptado")

try:
    if len(sys.argv) == 1:
        print(Fore.RED + "[-] Error de sintaxis")

    else:
        clave = sys.argv[1]
        directorio = sys.argv[2]

        if os.path.isdir(directorio):
            generarClave(clave)
            if os.path.isfile(clave):
                key = cargarClave(clave)

                archivos = []
                for i in os.listdir(directorio):
                    archivo = f"{directorio}/{i}"
                    if os.path.isfile(archivo):
                        archivos.append(archivo)

                encriptar(archivos, key)
            else:
                print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")

        else:
            print(Fore.RED + f"[-] Error al encontrar el directorio \"{directorio}\"")
except:
    print(Fore.RED + "error")
