import requests
import re
import sys
from urllib import request
from bs4 import BeautifulSoup
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def wgetNombre(url, extension):
    nombre = re.findall(f"/([a-zA-Z0-9_ ].+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]
    return nombre

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

if len(sys.argv) == 2:
    url = sys.argv[1]
elif len(sys.argv) == 3:
    url = sys.argv[1]
    ext = sys.argv[2]

valido, extension = getExt(url)

if valido and extension is not None and len(sys.argv) == 2:
    nombre = wgetNombre(url, extension)

    req = requests.get(url)

    with open(nombre, 'wb') as archivo:
        archivo.write(req.content)
    archivo.close()
    print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado correctamente")

elif not valido and extension is None and len(sys.argv) == 3:
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    archivos = getArchivos(soup, ext)
    for i in archivos:
        try:
            if ext == 'a':
                link = i.get("href")
            else:
                link = i.get("src")
            contenido = requests.get(link)
        except:
            if ext == 'a':
                link = url + i.get("href")
            else:
                link = url + i.get("src")
            contenido = requests.get(link)

        extension = getExt(link)[1]
        if extension is not None:
            nombre = wgetNombre(link, extension)
            with open(nombre, 'wb') as archivo:
                archivo.write(contenido.content)
            archivo.close()
            print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado")

elif not valido and extension is None and len(sys.argv) == 2:
    print(Fore.YELLOW +  "[!] warning")
    try:
        req = request.urlopen(url)

        nombre = input("Ingresa el nombre del archivo: ")
        with open(nombre, 'wb') as archivo:
            archivo.write(req.read())
        archivo.close()
        print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado")

    except Exception as e:
        print(e)

else:
    print(Fore.RED + "[-] error")
