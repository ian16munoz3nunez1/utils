import os
import sys
import re
from zipfile import ZipFile
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica la ubicacion de los archivos a comprimir")
    print(Fore.YELLOW + "* -o" + Fore.RED + " --> " + Fore.WHITE + "Especifica el archivo de salida en el que se comprimiran los archivos")

# La funcion 'getNombre' regresa el nombre de un archivo o directorio
def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(nombre)
    return nombre

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    m = re.split(r"(\s-[io]+[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    origen = params['-i']
    if '-o' in params.keys():
        destino = params['-o']
    else:
        destino = None

    return origen, destino

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

# Si se encuentra la bandera -h o --help en el comando se muestra ayuda para el usuario
if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

# Revisa que la bandera -i se encuentre en el comando
if not re.search(r"\s-i[= ]", cmd):
    print(Fore.RED + "[-] Ubicacion de archivo(s) a comprimir no ingresada")
    exit()

origen, destino = parametros(cmd) # Se obtienen los parametros ingresados por el usuario

# Si el origen es un archivo y el destino es un archivo zip...
if os.path.isfile(origen):
    try:
        if not re.search(r"\s-o[= ]", cmd):
            destino = getNombre(origen) + ".zip"

        # Se comprime el archivo
        with ZipFile(destino, 'w') as zip:
            zip.write(origen, getNombre(origen))
        zip.close()
        print(Fore.GREEN + f"[+] Archivo \"{origen}\" comprimido")

    except:
        print(Fore.RED + f"[-] Error al comprimir el archivo \"{origen}\"")

# Si el origen contiene '/', no es un directorio y el destino es un archivo zip...
elif re.search('/', origen) and not os.path.isdir(origen):
    # Si no se encuentra la bandera -o se termina la ejecucion del programa
    if not re.search(r"\s-o[= ]", cmd):
        print(Fore.RED + "[-] Nombre del archivo de salida no ingresado")
        exit()

    if not destino.endswith(".rar") and not destino.endswith(".zip"):
        destino = destino + ".zip"

    archivos = origen.split('/') # Se crea un arreglo de archivos
    cont = len(archivos)
    directorio = os.getcwd() # Se obtiene el directorio actual
    comprimidos = 0
    with ZipFile(destino, 'w') as zip:
        for i in archivos:
            archivo = f"{directorio}/{i}" # Se obtiene el path del archivo
            if os.path.isfile(archivo):
                zip.write(archivo, getNombre(archivo)) # Se comprime el arhivo
                print(Fore.GREEN + f"[+] Archivo \"{i}\" comprimido")
                comprimidos += 1
    zip.close()
    print(Fore.GREEN + f"[+] {comprimidos} archivos comprimidos de {cont}")

elif os.path.isdir(origen):
    try:
        if not re.search(r"\s-o[= ]", cmd):
            destino = getNombre(origen) + ".zip" # Se obtiene el destino de escritura

        if not destino.endswith(".rar") and not destino.endswith(".zip"):
            destino = destino + ".zip"
        cont = len(os.listdir(origen)) # Se obtiene el numero de elementos del directorio

        # Se crea una lista de archivos
        archivos = []
        for i in os.listdir(origen):
            archivo = f"{origen}/{i}"
            if os.path.isfile(archivo):
                archivos.append(archivo)

        # Se comprimen los archivos del directorio
        comprimidos = 0
        with ZipFile(destino, 'w') as zip:
            for i in archivos:
                zip.write(i, getNombre(i)) # Se comprime el archivo
                print(Fore.GREEN + f"[+] Archivo \"{i}\" comprimido")
                comprimidos += 1
        zip.close()

        print(Fore.GREEN + f"[+] {comprimidos} elementos comprimidos de {cont}")

    except:
        print(Fore.RED + f"[-] Error al comprimir el directorio \"{origen}\"")

else:
    print(Fore.RED + f"[-] Ubicacion \"{origen}\" no encontrada o problema con el parametro de destino")

