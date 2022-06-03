import os
import sys
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def cargarClave(clave):
    return open(clave, 'rb').read()

def desencriptar(archivos, key):
    f = Fernet(key)

    for i in archivos:
        nombre = os.path.basename(i)
        with open(i, 'rb') as archivo:
            data = archivo.read()
        archivo.close()

        dataDecrypt = f.decrypt(data)

        with open(i, 'wb') as archivo:
            archivo.write(dataDecrypt)
        archivo.close()

        print(Fore.GREEN + f"[+] Archivo \"{nombre}\" desencriptado")

try:
    if len(sys.argv) == 1:
        print(Fore.RED + "Error de sintaxis")

    else:
        clave = sys.argv[1]
        directorio = sys.argv[2]

        if os.path.isdir(directorio):
            if os.path.isfile(clave):
                print(Fore.YELLOW + f"[!] Segur@ que quieres usar la clave \"{clave}\"?...\n[S/n]", end='')
                res = input()

                if len(res) == 0 or res.upper() == 'S':
                    key = cargarClave(clave)

                    archivos = []
                    for i in os.listdir(directorio):
                        archivo = f"{directorio}/{i}"
                        if os.path.isfile(archivo):
                            archivos.append(archivo)

                    desencriptar(archivos, key)

                    os.remove(clave)
                    print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
                else:
                    print(Fore.YELLOW + "Desencriptacion cancelada")
        else:
            print(Fore.RED + f"[-] Error al encontrar el directorio \"{directorio}\"")

except:
    print(Fore.RED + "error")
