import os
import sys
from zipfile import ZipFile
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

archivo = sys.argv[1]
directorio = sys.argv[2]

if os.path.isfile(archivo):
    if not os.path.isdir(directorio):
        os.mkdir(directorio)

    cont = 0
    with ZipFile(archivo, 'r') as zip:
        for i in zip.namelist():
            zip.extract(i, directorio)
            print(Fore.GREEN + f"[+] Archivo \"{i}\" descomprimido")
            cont += 1
    zip.close()

    print(f"[+] {cont} archivos descomprimidos")
else:
    print(Fore.RED + f"[-] Archivo \"{archivo}\" no encontrado")
