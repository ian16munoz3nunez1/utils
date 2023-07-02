import os
import sys
import re
from zipfile import ZipFile
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica la ubicacion del archivo a descomprimir")
    print(Fore.YELLOW + "* -o" + Fore.RED + " --> " + Fore.WHITE + "Especifica el directorio de salida en el que se descomprimiran los archivos")

# La funcion 'getNombre' regresa el nombre de un archivo o directorio
def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(nombre)
    return nombre

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    if re.search(r"\s-p\s?", cmd):
        m = re.search(r"\s-p\s?", cmd)
        if m.end() == len(cmd):
            filtros = cmd[m.start()+1:m.end()]
            cmd = re.sub(r"\s-p", '', cmd)
        else:
            filtros = cmd[m.start()+1:m.end()-1]
            cmd = re.sub(r"\s-p\s?", ' ', cmd)

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

# Si se encuentra la bandera -h o --help se muestra ayuda para el usuario
if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

if not re.search(r"\s-i[= ]", cmd):
    print(Fore.RED + "[-] Ubicacion de archivo(s) a comprimir no ingresada")
    exit()

origen, destino = parametros(cmd)

# Si el origen es un archivo zip
if os.path.isfile(origen):
    if re.search(r"\s-p\s?", cmd):
        cont = 0
        with ZipFile(origen, 'r') as zip:
            for i in zip.namelist():
                print(Fore.CYAN + f"[*] {i}")
                cont += 1
        zip.close()
        print(Fore.CYAN + f"[*] {cont} archivos contenidos")
        exit()

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

    print(Fore.GREEN + f"[+] {descomprimidos} archivos descomprimidos")

else:
    print(Fore.RED + f"[-] Archivo \"{origen}\" no encontrado")

