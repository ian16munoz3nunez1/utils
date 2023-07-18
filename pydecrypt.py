# Ian Mu;oz Nu;ez

import os
import sys
import re
from cryptography.fernet import Fernet
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra una ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica el archivo o directorio a desencriptar")
    print(Fore.YELLOW + "* -k" + Fore.RED + " --> " + Fore.WHITE + "Especifica el nombre de la clave de encriptacion")

# La funcion 'cargarClave' carga la clave del archivo de encriptacion
def cargarClave(clave):
    return open(clave, 'rb').read()

# La funcion 'desencriptar' desencripta el arreglo de archivos 'archivos' con la clave 'key'
def desencriptar(archivos, key):
    f = Fernet(key)
    cont = 0
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
        cont += 1

    print(Fore.GREEN + f"[+] {cont} archivos desencriptados")

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

clave, ubicacion = parametros(cmd)

# Si la clave no tiene la extension '.key' se agrega
if not clave.endswith(".key"):
    clave += ".key"

if not os.path.isfile(clave):
    print(Fore.RED + f"[-] Error al encontrar la clave \"{clave}\"")
    print(Fore.YELLOW + "[!] Desencriptacion cancelada")
    exit()

print(Fore.GREEN + f"[+] Clave \"{clave}\" encontrada")

# Si la ubicacion ingresada es un archivo...
if os.path.isfile(ubicacion):
    print(Fore.YELLOW + f"[!] Segur@ que quieres desencriptar el archivo \"{ubicacion}\"?...\n[S/n]", end=' ')
    res = input()

    if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
        key = cargarClave(clave) # Se carga la clave
        desencriptar([ubicacion], key) # Se desencripta el archivo

        os.remove(clave) # Se elimina la clave ingresada
        print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")
    else:
        print(Fore.YELLOW + "[!] Desencriptacion cancelada")

# Si la ubicacion ingresada es un directorio...
elif os.path.isdir(ubicacion):
    print(Fore.YELLOW + f"[!] Segur@ que quieres desencriptar el directorio \"{ubicacion}\"?...\n[S/n]", end=' ')
    res = input()

    if len(res) == 0 or res.upper() == 'S' or res.upper()[0] == 'S':
        key = cargarClave(clave) # Se carga la clave

        # Se crea una lista de archivos
        archivos = []
        for i in os.listdir(ubicacion):
            archivo = f"{ubicacion}/{i}"
            if os.path.isfile(archivo) and not i.endswith(".key"):
                archivos.append(archivo)

        desencriptar(archivos, key) # Se desencriptan los archivos

        os.remove(clave) # Se elimina la clave ingresada
        print(Fore.YELLOW + f"[!] Clave \"{clave}\" eliminada")

    else:
        print(Fore.YELLOW + "[!] Desencriptacion cancelada")

else:
    print(Fore.RED + f"[-] Error al encontrar la ubicacion \"{ubicacion}\"")

