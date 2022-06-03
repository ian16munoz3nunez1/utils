import os
import sys
from zipfile import ZipFile
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

directorio = sys.argv[1]
archivo = sys.argv[2]

if os.path.isdir(directorio):
    cont = 0
    with ZipFile(archivo, 'w') as zip:
        for i in os.listdir(directorio):
            path = f"{directorio}/{i}"
            if os.path.isfile(path):
                zip.write(path, i)
                print(Fore.GREEN + f"[+] Archivo \"{i}\" comprimido")
                cont += 1
    zip.close()

    print(Fore.GREEN + f"[+] {cont} archivos comprimidos")

else:
    print(Fore.RED + f"[-] Directorio \"{directorio}\" no encontrado")
