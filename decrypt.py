import os
import sys
import re
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# 'cargarClave' carga la llave del archivo de encriptacion
def cargarClave(clave):
    return open(clave, 'rb').read()

# 'desencriptar' desencripta el arreglo de archivos 'archivos' con la llave 'key'
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

# Se obtiene el comando ingresado
cmd = ''.join(' ' + i for i in sys.argv)
try:
    mKey = re.search("-k[= ]", cmd)
    mUbicacion = re.search("-p[= ]", cmd)

    # Se obtienen los parametros del comando
    clave = ''
    ubicacion = ''
    if mKey.start() < mUbicacion.start():
        clave = cmd[mKey.end():mUbicacion.start()-1]
        ubicacion = cmd[mUbicacion.end():]
    if mUbicacion.start() < mKey.start():
        ubicacion = cmd[mUbicacion.end():mKey.start()-1]
        clave = cmd[mKey.end():]

except:
    exit()

# Se revisa si los parametros y la sintaxis son correctos
if re.search("-k[= ]", cmd) and re.search("-p[= ]", cmd):
    # Si la ubicacion ingresada es un archivo...
    if os.path.isfile(ubicacion) and clave.endswith(".key"):
        if os.path.isfile(clave):
            print(Fore.YELLOW + f"[!] Segur@ que quieres desencriptar el archivo \"{ubicacion}\"?...\n[S/n]", end=' ')
            res = input() # Se espera una respuesta

            if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
                key = cargarClave(clave) # Se carga la llave
                desencriptar([ubicacion], key) # Se encripta el archivo

                os.remove(clave) # Se elimina la llave ingresada
                print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
            else:
                print(Fore.YELLOW + "[!] Desencriptacion cancelada")

        else:
            print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
            print(Fore.YELLOW + "[!] Desencriptacion cancelada")

    # Si la ubicacion ingresada es un directorio...
    elif os.path.isdir(ubicacion) and clave.endswith(".key"):
        if os.path.isfile(clave):
            print(Fore.YELLOW + f"[!] Segur@ que quieres usar la clave \"{clave}\"?...\n[S/n]", end=' ')
            res = input() # Se espera una respuesta

            if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
                key = cargarClave(clave) # Se carga la llave

                # Se crea una lista de archivos
                archivos = []
                for i in os.listdir(ubicacion):
                    archivo = f"{ubicacion}/{i}"
                    if os.path.isfile(archivo) and not i.endswith(".key"):
                        archivos.append(archivo)

                desencriptar(archivos, key) # Se desencriptan los archivos

                os.remove(clave) # Se elimina la llave ingresada
                print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")

            else:
                print(Fore.YELLOW + "[!] Desencriptacion cancelada")
        else:
            print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")

    else:
        print(Fore.RED + f"[-] Error al encontrar la ubicacion \"{ubicacion}\"")
else:
    print(Fore.RED + "[-] Error de sintaxis")

