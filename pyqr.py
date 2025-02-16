#!python3

# Ian Mu;oz Nu;ez

import sys
import pyqrcode
import png
from pyqrcode import QRCode
import re
from colorama import init
from colorama.ansi import Fore

init(autoreset=True) # Configuracion de colorama

def manual():
    print(Fore.YELLOW + "* -u" + Fore.RED + " --> " + Fore.WHITE + "URL")
    print(Fore.GREEN + "+ -n" + Fore.RED + " --> " + Fore.WHITE + "Nombre de archivo")

# Regresa los parametros ingresados en el comando
def parametros(cmd):
    m = re.split(r"(\s-[nu]+[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    url = params['-u']
    if not '-n' in params:
        nombre = "qrcode.png"
    else:
        nombre = params['-n']

    return url, nombre

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

# Se revisa que la bandera -u se encuentre en el comando
if not re.search(r"\s-u[= ]", cmd):
    print(Fore.RED + "[-] URL no ingresada")
    exit()

url, nombre = parametros(cmd) # URL y nombre de archivo para guardar

url = pyqrcode.create(url) # Codigo QR

# Si es posible, se guarda el QR
if nombre.endswith(".png"):
    url.png(nombre, scale=8)
elif nombre.endswith(".svg"):
    url.svg(nombre, scale=8)
else:
    print(Fore.YELLOW + f"[!] warning: Extension de archivo incorrecta: '{nombre}'")

