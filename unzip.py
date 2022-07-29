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

if re.search(r"\s-i[= ]", cmd):
    origen, destino = parametros(cmd)

    # Si el origen es un archivo zip
    if os.path.isfile(origen):
        if not re.search(r"\s-o[= ]", cmd):
            destino = getNombre(origen).replace(".zip", '')
        # Si el directorio destino no existe se crea
        if not os.path.isdir(destino):
            os.mkdir(destino)

        descomprimidos = 0
        with ZipFile(origen, 'r') as zip: # Se crea la instancia del archivo 'origen'
            for i in zip.namelist():
                zip.extract(i, destino) # Se descomprime el archivo 'i' en 'destino'
                print(Fore.GREEN + f"[+] Archivo \"{i}\" descomprimido")
                descomprimidos += 1
        zip.close()

        print(f"[+] {descomprimidos} archivos descomprimidos")

    else:
        print(Fore.RED + f"[-] Archivo \"{origen}\" no encontrado")

else:
    print(Fore.RED + "[-] error de sintaxis")

