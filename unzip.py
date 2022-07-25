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
    try:
        origen = re.findall("-i[= ]([\W\w]+) -o", cmd)[0]
    except:
        origen = re.findall("-i[= ]([\W\w]+)", cmd)[0]

    try:
        destino = re.findall("-o[= ]([\W\w]+) -i", cmd)[0]
    except:
        destino = re.findall("-o[= ]([\W\w]+)", cmd)[0]

    return origen, destino

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

if re.search("-i[= ]", cmd) and re.search("-o[= ]", cmd):
    origen, destino = params(cmd)

    # Si el origen es un archivo zip
    if os.path.isfile(origen) and (origen.endswith(".zip") or origen.endswith(".rar")):
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

