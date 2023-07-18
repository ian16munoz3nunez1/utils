# Ian Mu;oz Nu;ez

import os
import sys
import re
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica el archivo o directorio a encriptar")
    print(Fore.YELLOW + "* -k" + Fore.RED + " --> " + Fore.WHITE + "Especifica el nombre de la clave de encriptacion")

# La funcion 'generarClave' crea un archivo .key en el que se almacena la clave de encriptacion
def generarClave(clave):
    try:
        key = Fernet.generate_key()

        with open(clave, 'wb') as keyFile:
            keyFile.write(key)
        keyFile.close()

        print(Fore.GREEN + f"[+] Clave \"{clave}\" generada correctamente")

    except:
        pass

# La funcion 'cargarClave' carga la clave del archivo de encriptacion
def cargarClave(clave):
    return open(clave, 'rb').read()

# La funcion 'encriptar' encripta todos los elementos del arreglo 'archivos' con la clave 'key'
def encriptar(archivos, key):
    f = Fernet(key)
    cont = 0
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
        cont += 1

    print(Fore.GREEN + f"[+] {cont} archivos encriptados")

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    m = re.split(r"(\s-[ik]+[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    ubicacion = params['-i']
    clave = params['-k']

    return clave, ubicacion

# Se obtiene el comando ingresado
cmd = ''.join(' ' + i for i in sys.argv)

# Si se encuentra la bandera -h o --help se muestra ayuda para el usuario
if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

# Se revisa que la bandera -i se encuentre en el comando
if not re.search(r"\s-i[= ]", cmd):
    print(Fore.RED + "[-] Ubicacion del archivo o directorio no ingresada")
    exit()

# Se revisa que la bandera -k se encuentre en el comando
if not re.search(r"\s-k[= ]", cmd):
    print(Fore.RED + "[-] Nombre de la clave de encriptacion no ingresado")
    exit()

clave, ubicacion = parametros(cmd) # Se obtienen los parametros del comando

# Si la clave no tiene la extension '.key' se agrega
if not clave.endswith(".key"):
    clave += ".key"

# Si la ubicacion ingresada es un archivo...
if os.path.isfile(ubicacion):
    generarClave(clave) # Se genera una nueva clave
    if os.path.isfile(clave):
        print(Fore.YELLOW + f"[!] Segur@ que quieres encriptar el archivo \"{ubicacion}\"?...\n[S/n]", end=' ')
        res = input()

        if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
            key = cargarClave(clave) # Se carga la clave
            encriptar([ubicacion], key) # Se encripta el archivo
        else:
            os.remove(clave) # Se elimina la ultima llave creada
            print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
            print(Fore.YELLOW + "[!] Encriptacion cancelada")
    else:
        print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
        print(Fore.YELLOW + "[!] Encriptacion cancelada")

# Si la ubicacion ingresada es un directorio...
elif os.path.isdir(ubicacion) and clave.endswith(".key"):
    # Se crea una lista de archivos
    archivos = []
    for i in os.listdir(ubicacion):
        archivo = f"{ubicacion}/{i}"
        if os.path.isfile(archivo):
            archivos.append(archivo)

    generarClave(clave) # Se genera una nueva clave
    if os.path.isfile(clave):
        print(Fore.YELLOW + f"[!] Segur@ que quieres encriptar el directorio \"{ubicacion}\"?...\n[S/n]", end=' ')
        res = input()

        if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
            key = cargarClave(clave) # Se carga la clave
            encriptar(archivos, key) # Se encriptan los archivos
        else:
            os.remove(clave) # Se elimina la ultima clave creada
            print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
            print(Fore.YELLOW + f"[!] Encriptacion cancelada")

    else:
        print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
        print(Fore.YELLOW + "[!] Encriptacion cancelada")

else:
    print(Fore.RED + f"[-] Error al encontrar la ubicacion \"{ubicacion}\" o la llave \"{clave}\"")

