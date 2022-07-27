import os
import sys
import re
from zipfile import ZipFile
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# 'getNombre' regresa el nombre de un archivo o directorio
def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(nombre)
    return nombre

def params(cmd):
    m = re.split(r"(\s-[io]?[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    origen = params['-i']
    destino = params['-o']

    return origen, destino

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

if re.search(r"\s-i[= ]", cmd) and re.search(r"\s-o[= ]", cmd):
    origen, destino = params(cmd)

    # Si el origen es un archivo y el destino es un archivo zip...
    if os.path.isfile(origen) and (destino.endswith(".zip") or destino.endswith(".rar")):
        try:
            # Se comprime el archivo
            with ZipFile(destino, 'w') as zip:
                zip.write(origen, getNombre(origen))
            zip.close()
            print(Fore.GREEN + f"[+] Archivo \"{origen}\" comprimido")

        except:
            print(Fore.RED + f"[-] Error al comprimir el archivo \"{origen}\"")

    # Si el origen contiene '/', no es un directorio y el destino es un archivo zip...
    elif re.search('/', origen) and not os.path.isdir(origen) and (destino.endswith(".zip") or destino.endswith(".rar")):
        try:
            archivos = origen.split('/') # Se crea un arreglo de archivos
            directorio = os.getcwd() # Se obtiene el directorio actual
            with ZipFile(destino, 'w') as zip:
                for i in archivos:
                    archivo = f"{directorio}/{i}" # Se obtiene el path del archivo
                    if os.path.isfile(archivo):
                        zip.write(archivo, getNombre(archivo)) # Se comprime el arhivo
                        print(Fore.GREEN + f"[+] Archivo \"{i}\" comprimido")
            zip.close()

        except:
            print(Fore.RED + f"[-] Error al comprimir los archivos")

    elif os.path.isdir(origen) and (destino.endswith(".zip") or destino.endswith(".rar")):
        try:
            cont = len(os.listdir(origen)) # Se obtiene el numero de elementos del directorio
            # Se crea una lista de archivos
            archivos = []
            for i in os.listdir(origen):
                archivo = f"{origen}/{i}"
                if os.path.isfile(archivo):
                    archivos.append(archivo)

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
else:
    print(Fore.RED + "Error de sintaxis")

