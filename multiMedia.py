import cv2
import numpy
import sys
import os
import re
from random import randint
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

def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(ubicacion)

    return nombre

def isImage(ubicacion):
    ext = [".jpg", ".png", ".jpeg", ".webp", ".JPG", ".PNG", ".JPEG", ".WEBP"]

    imagen = False
    for i in ext:
        if ubicacion.endswith(i):
            imagen = True
            break

    return imagen

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

def parametros(cmd):
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

    m = re.split(r"(\s-[it]+[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    ubicacion = params['-i']
    if '-t' in params.keys():
        try:
            escala = float(params['-t'])
        except:
            pass

    return ubicacion, escala, filtros

cmd = ''.join(' ' + i for i in sys.argv)

if re.search(r"\s-i[= ]", cmd):
    ubicacion, escala, filtros = parametros(cmd)

    if os.path.isdir(ubicacion):
        archivos = []
        for i in os.listdir(ubicacion):
            archivo = f"{ubicacion}/{i}"
            if os.path.isfile(archivo) and isImage(i):
                archivos.append(archivo)

        numero = randint(0, len(archivos)-1)
        archivo = archivos[numero]

        imagen = cv2.imread(archivo)
        height, width = imagen.shape[:2]

        if escala is None:
            escala = escalar(height, width)
            imagen = cv2.resize(imagen, None, fx=escala, fy=escala)
        else:
            imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

        if filtros:
            imagen = filtrar(imagen, filtros)

        print(Fore.CYAN + "[*] Ubicacion:", archivo)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        nombre = getNombre(archivo)
        cv2.imshow(nombre, imagen)
        cv2.waitKey()
        cv2.destroyAllWindows()

    elif os.path.isfile(ubicacion) and isImage(ubicacion):
        imagen = cv2.imread(ubicacion)
        height, width = imagen.shape[:2]

        if escala is None:
            escala = escalar(height, width)
            imagen = cv2.resize(imagen, None, fx=escala, fy=escala)
        else:
            imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

        if filtros:
            imagen = filtrar(imagen, filtros)

        print(Fore.CYAN + "[*] Ubicacion:", ubicacion)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        nombre = getNombre(ubicacion)
        cv2.imshow(nombre, imagen)
        cv2.waitKey()
        cv2.destroyAllWindows()

    else:
        print(Fore.RED + f"[-] Ubicacion \"{ubicacion}\" no encontrada o incompatible")

else:
    print(Fore.RED + "[-] Error de sintaxis (falta del parametro '-i')")
