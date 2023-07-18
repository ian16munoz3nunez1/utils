# Ian Mu;oz Nu;ez

import requests
import re
import sys
from urllib import request
from bs4 import BeautifulSoup
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -u" + Fore.RED + " --> " + Fore.WHITE + "Especifica la URL del archivo a descargar")
    print(Fore.GREEN + "+ -n" + Fore.RED + " --> " + Fore.WHITE + "Especifica el nombre con el que se quiere nombrar el archivo a descargar")
    print(Fore.GREEN + "+ -x" + Fore.RED + " --> " + Fore.WHITE + "Si se quieren los archivos de una pagina, espeficia el tipo de archivos que se quieren descargar")

# La funcion 'wgetNombre' regresa el nombre de una URL para nombrar el archivo a descargar
def wgetNombre(url, extension):
    nombre = re.findall(f"/([a-zA-Z0-9_ ].+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]
    return nombre

# La funcion 'getExt' regresa si la URL es valida y la extension del archivo de esta URL
def getExt(url):
    extensiones = ["jpg", "png", "jpeg", "svg", "webp", "mp4", "avi", "mkv",
        "html", "css", "txt", "dat", "py", "java", "c", "cpp", "js", "ino",
        "go", "rb", "m", "h", "pdf", "docx", "pptx", "xlsx", "odt", "ods", "odp",
        "odg", "xcf", "gif", "webm", "mp3", "opus", "mpga", "wav"]
    upperExtensiones = [i.upper() for i in extensiones]

    valido = False
    extension = None
    i = 0
    while i < len(extensiones):
        if re.search(f"[.]{extensiones[i]}", url):
            valido = True
            extension = extensiones[i]
            break
        if re.search(f"[.]{upperExtensiones[i]}", url):
            valido = True
            extension = upperExtensiones[i]
            break
        i += 1

    return valido, extension

# Si se quieren descargar los archivos de una pagina, la funcion 'getArchivos' regresa
# una lista de los archivos de esta
def getArchivos(soup, ext):
    if ext == '*':
        archivos = []
        img = soup.find_all("img")
        video = soup.find_all("video")
        audio = soup.find_all("audio")
        for i in img:
            archivos.append(i)
        for i in video:
            archivos.append(i)
        for i in audio:
            archivos.append(audio)
    else:
        archivos = soup.find_all(ext)

    return archivos

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    ext = None
    nombre = None

    m = re.split(r"(\s-[nux]+[= ])", cmd)
    m.pop(0)

    params = {}
    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    url = params['-u']
    if '-n' in params.keys():
        nombre = params['-n']
    if '-x' in params.keys():
        ext = params['-x']

    return url, ext, nombre

cmd = ''.join(' ' + i for i in sys.argv)

# Si se encuentra la bandera -h o --help se muestra ayuda para el usuario
if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

# Revisa que la bandera -u se encuentre en el comando
if not re.search(r"\s-u[= ]", cmd):
    print(Fore.RED + "[-] Direccion URL no ingresada")
    exit()

if re.search(r"\s-n[= ]", cmd) and re.search(r"\s-x[= ]", cmd):
    print(Fore.YELLOW + "[!] Los parametros -n y -x entran en conflicto")
    exit()

url, ext, nombre = parametros(cmd) # Se obtienen los parametros ingresados por el usuario

if not re.search(r"\s-n[= ]", cmd) and not re.search(r"\s-x[= ]", cmd):
    extension = getExt(url)[1]
    nombre = wgetNombre(url, extension)

    req = requests.get(url)

    with open(nombre, 'wb') as archivo:
        archivo.write(req.content)
    archivo.close()
    print(Fore.GREEN + f"[+] Archivo \"{nombre}\" descargado correctamente")

elif re.search(r"\s-x[= ]", cmd):
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "html.parser")

        archivos = getArchivos(soup, ext)
        cont = 0
        for i in archivos:
            if ext == 'a':
                x = i.get('href')
            else:
                x = i.get('src')

            if x[:4] == 'http':
                if ext == 'a':
                    link = i.get('href')
                else:
                    link = i.get('src')
            else:
                if ext == 'a':
                    link = url + i.get('href')
                else:
                    link = url + i.get('src')
            contenido = requests.get(link)

            nombre = link.split('/')[-1]
            with open(nombre, 'wb') as archivo:
                archivo.write(contenido.content)
            archivo.close()
            print(Fore.GREEN + f"[+] Link \"{link}\" descargado correctamente")
            cont += 1

        print(Fore.GREEN + f"[+] {cont} archivos descargados")

    except Exception as e:
        e = str(e)
        print(Fore.RED + e)

elif re.search(r"\s-n[= ]", cmd):
    try:
        req = request.urlopen(url)

        with open(nombre, 'wb') as archivo:
            archivo.write(req.read())
        archivo.close()
        print(Fore.GREEN + f"[+] Archivo \"{nombre}\" descargado correctamente")

    except Exception as e:
        e = str(e)
        print(Fore.RED + e)

else:
    print(Fore.RED + "[-] error")

