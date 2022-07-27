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

def filtrar(imagen, f):
    if re.search(r'90', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search(r'180', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_180)
    if re.search(r'270', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    if re.search(r'x', f):
        imagen = cv2.flip(imagen, 0)
    if re.search(r'y', f):
        imagen = cv2.flip(imagen, 1)
    if re.search(r'g', f):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    if re.search(r'n', f):
        imagen = 255 - imagen
    if re.search(r'm', f):
        flip = cv2.flip(imagen, 1)
        imagen = numpy.hstack((imagen, flip))
    if re.search(r'c', f):
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (3,3), 0)
        t1 = int(input("Threshold1: "))
        t2 = int(input("Threshold2: "))
        canny = cv2.Canny(image=blur, threshold1=t1, threshold2=t2)
        imagen = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    return imagen


def params(cmd):
    escala = None
    filtros = None

    if re.search(r"\s-[xygnmc012789]+\s?", cmd):
        m = re.search(r"\s-[xygnmc012789]+\s?", cmd)
        if m.end() == len(cmd):
            filtros = cmd[m.start()+1:m.end()]
            cmd = re.sub(r"\s-[xygnmc012789]+", '', cmd)
        else:
            filtros = cmd[m.start()+1:m.end()-1]
            cmd = re.sub(r"\s-[xygnmc012789]+\s?", ' ', cmd)

    m = re.split(r"(\s-[tu]?[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    if '-t' in params.keys():
        escala = float(params['-t'])
    url = params['-u']

    return url, escala, filtros

cmd = ''.join(' ' + i for i in sys.argv)

if re.search(r"\s-u[= ]", cmd):
    url, escala, filtros = params(cmd)
    valido, extension = getExt(url)

    if valido:
        nombre = re.findall(f"/([\W\w]+[.]{extension})", url)[0]
        nombre = nombre.split('/')[-1]

        req = requests.get(url)
        matriz = numpy.frombuffer(req.content, dtype=numpy.uint8)

        imagen = cv2.imdecode(matriz, -1)
        height, width = imagen.shape[:2]

        if not escala:
            escala = escalar(height, width)
        imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

        if filtros:
            imagen = filtrar(imagen, filtros)

        print(Fore.CYAN + "[*] Nombre:", nombre)
        print(Fore.CYAN + "[*] Escala:", escala)
        cv2.imshow(nombre, imagen)
        cv2.waitKey()
        cv2.destroyAllWindows()

    else:
        print("error")

else:
    print(Fore.RED + "[-] error de sintaxis")

