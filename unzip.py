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

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

# Se revisa si la sintaxis y los parametros son correctos
try:
    mOrigen = re.search("-o[= ]", cmd)
    mDestino = re.search("-d[= ]", cmd)

    origen = ''
    destino = ''
    if mOrigen.start() < mDestino.start():
        origen = cmd[mOrigen.end():mDestino.start()-1]
        destino = cmd[mDestino.end():]
    if mDestino.start() < mOrigen.start():
        destino = cmd[mDestino.end():mOrigen.start()-1]
        origen = cmd[mOrigen.end():]

except:
    print(Fore.RED + "[-] Error de sintaxis")
    exit()

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
