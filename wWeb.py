import cv2
import numpy
import sys
import re
import requests
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def escalar(height, width):
    if height > width:
        escala = 600/height
    elif width > height:
        escala = 600/width
    else:
        escala = 600/height

    return escala

def getExt(url):
    extensiones = ["jpg", "png", "jpeg", "webp"]
    exntensionesUpper = [i.upper() for i in extensiones]

    valido = False
    extension = None
    i = 0
    while i < len(extensiones):
        if re.search(f"[.]{extensiones[i]}", url):
            valido = True
            extension = extensiones[i]
            break
        if re.search(f"[.]{extensionesUpper[i]}", url):
            valido = True
            extension = extensionesUpper[i]
            break
        i += 1

    return valido, extension

def params(cmd):
    escala = None

    try:
        url = re.findall("-u[= ]([\W\w]+) -[txygnmc012789]", cmd)[0]
    except:
        url = re.findall("-u[= ]([\W\w]+)", cmd)[0]

    if re.search("-t[= ]", cmd):
        try:
            escala = float(re.findall("-t[= ]([.0-9]+) -[uxygnmc012789]+", cmd)[0])
        except:
            escala = float(re.findall("-t[= ]([.0-9]+)", cmd)[0])

    return url, escala

cmd = ''.join(' ' + i for i in sys.argv)

url, escala = params(cmd)
valido, extension = getExt(url)

if valido:
    nombre = re.findall(f"/([\W\w]+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]

    req = requests.get(url)
    matriz = numpy.frombuffer(req.content, dtype=numpy.uint8)

    imagen = cv2.imdecode(matriz, -1)
    height, width = imagen.shape[:2]

    if escala is None:
        escala = escalar(height, width)
    imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

    print(Fore.CYAN + "[*] Nombre:", nombre)
    print(Fore.CYAN + "[*] Escala:", escala)
    cv2.imshow(nombre, imagen)
    cv2.waitKey()
    cv2.destroyAllWindows()

else:
    print("error")
