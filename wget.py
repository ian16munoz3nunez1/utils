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

def params(cmd):
    ext = None
    nombre = None

    try:
        url = re.findall("-u[= ]([\W\w]+) -[nx]+", cmd)[0]
    except:
        url = re.findall("-u[= ]([\W\w]+)", cmd)[0]

    if re.search("-x[= ]", cmd):
        try:
            ext = re.findall("-x[= ]([\W\w]+) -[nu]+", cmd)[0]
        except:
            ext = re.findall("-x[= ]([\W\w]+)", cmd)[0]

    if re.search("-n[= ]", cmd):
        try:
            nombre = re.findall("-n[= ]([\W\w]+) -[ux]+", cmd)[0]
        except:
            nombre = re.findall("-n[= ]([\W\w]+)", cmd)[0]

    return url, ext, nombre

cmd = ''.join(' ' + i for i in sys.argv)

if re.search("-u[= ]", cmd):
    url, ext, nombre = params(cmd)

    valido, extension = getExt(url)

    if re.search("-n[= ]", cmd) and re.search("-x[= ]", cmd):
        print(Fore.YELLOW + "[!] El nombre y la extension entran en conflicto")
        exit()

    if valido and extension is not None and not re.search("-n[= ]", cmd):
        nombre = wgetNombre(url, extension)

        req = requests.get(url)

        with open(nombre, 'wb') as archivo:
            archivo.write(req.content)
        archivo.close()
        print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado correctamente")

    elif not valido and extension is None and re.search("-x[= ]", cmd):
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

    elif re.search("-n[= ]", cmd) and nombre is not None:
        try:
            req = request.urlopen(url)

            with open(nombre, 'wb') as archivo:
                archivo.write(req.read())
            archivo.close()
            print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado")

        except Exception as e:
            print(e)

    else:
        print(Fore.RED + "[-] error")

else:
    print(Fore.RED + "[-] error de sintaxis")
