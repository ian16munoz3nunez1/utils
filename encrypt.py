import os
import sys
import re
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# 'generarClave' crea un archivo .key en el que se almacena la llave de encriptacion
def generarClave(clave):
    try:
        key = Fernet.generate_key()

        with open(clave, 'wb') as keyFile:
            keyFile.write(key)
        keyFile.close()

        print(Fore.GREEN + f"[+] Clave \"{clave}\" generada")

    except:
        pass

# 'cargarClave' carga la llave del archivo de encriptacion
def cargarClave(clave):
    return open(clave, 'rb').read()

# 'encriptar' encripta todos los elementos del arreglo 'archivos' con la llave 'key'
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
    # Se obtiene el comando ingresado
    cmd = ''.join(' ' + i for i in sys.argv)

    # Se revisa si los parametros y la sintaxis son correctos
    if re.search("-k[= ]", cmd) and re.search("-p[= ]", cmd):
        mKey = re.search("-k[= ]", cmd)
        mUbicacion = re.search("-p[= ]", cmd)

        # Se obtienen los parametros
        clave = ''
        ubicacion = ''
        if mKey.start() < mUbicacion.start():
            clave = cmd[mKey.end():mUbicacion.start()-1]
            ubicacion = cmd[mUbicacion.end():]
        if mUbicacion.start() < mKey.start():
            ubicacion = cmd[mUbicacion.end():mKey.start()-1]
            clave = cmd[mKey.end():]

        # Si la ubicacion ingresada es un archivo...
        if os.path.isfile(ubicacion) and clave.endswith(".key"):
            generarClave(clave) # Se genera una nueva llave
            if os.path.isfile(clave):
                print(Fore.YELLOW + f"[!] Segur@ que quieres encriptar el archivo \"{ubicacion}\"?...\n[S/n]", end=' ')
                res = input() # Se espera una respuesta

                if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
                    key = cargarClave(clave) # Se carga la llave
                    encriptar([ubicacion], key) # Se encripta el archivo
                else:
                    os.remove(clave) # Se elimina la ultima llave creada
                    print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
                    print(Fore.YELLOW + "[!] Encriptacion cancelada")
            else:
                print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
                print(Fore.YELLOW + "[!] Encriptacion cancelada")

        # Si la ubicacion ingresada es un directorio
        elif os.path.isdir(ubicacion) and clave.endswith(".key"):
            # Se crea una lista de archivos
            archivos = []
            for i in os.listdir(ubicacion):
                archivo = f"{ubicacion}/{i}"
                if os.path.isfile(archivo):
                    archivos.append(archivo)

            generarClave(clave) # Se genera una nueva llave
            if os.path.isfile(clave):
                print(Fore.YELLOW + f"[!] Segur@ que quieres encriptar el directorio \"{ubicacion}\"?...\n[S/n]", end=' ')
                res = input() # Se espera una respuesta

                if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
                    key = cargarClave(clave) # Se carga la llave
                    encriptar(archivos, key) # Se encriptan los archivos
                else:
                    os.remove(clave) # Se elimina la ultima llave creada
                    print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
                    print(Fore.YELLOW + f"[!] Encriptacion cancelada")

            else:
                print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
                print(Fore.YELLOW + "[!] Encriptacion cancelada")

        else:
            print(Fore.RED + f"[-] Error al encontrar la ubicacion \"{ubicacion}\" o la llave \"{clave}\"")
    else:
        print(Fore.RED + "[-] Error de sintaxis")

except:
    print(Fore.RED + "error")
