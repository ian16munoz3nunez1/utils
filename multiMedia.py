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
    if re.search('90', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search('180', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_180)
    if re.search('270', f):
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    if re.search('x', f):
        imagen = cv2.flip(imagen, 0)
    if re.search('y', f):
        imagen = cv2.flip(imagen, 1)
    if re.search('g', f):
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    if re.search('n', f):
        imagen = 255 - imagen
    if re.search('m', f):
        flip = cv2.flip(imagen, 1)
        imagen = numpy.hstack((imagen, flip))
    if re.search('c', f):
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (3,3), 0)
        t1 = int(input("Threshold1: "))
        t2 = int(input("Threshold2: "))
        canny = cv2.Canny(image=blur, threshold1=t1, threshold2=t2)
        imagen = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    return imagen

def params(cmd):
    ubicacion = None
    escala = None
    filtros = None

    try:
        ubicacion = re.findall(r"-i[= ]([\W\w]+) -[txygnmc012789]+", cmd)[0]
    except:
        ubicacion = re.findall(r"-i[= ]([\W\w]+)", cmd)[0]

    if re.search("-t[= ]", cmd):
        try:
            escala = float(re.findall("-t[= ]([.0-9]+) -[ixygnmc012789]+", cmd)[0])
        except:
            escala = float(re.findall("-t[= ]([.0-9]+)", cmd)[0])

    if re.search("-[xygnmc012789]+", cmd):
        try:
            filtros = re.findall("-([xygnmc012789]+) -[it]+", cmd)[0]
        except:
            filtros = re.findall("-([xygnmc012789]+)", cmd)[0]

    return ubicacion, escala, filtros

cmd = ''.join(' ' + i for i in sys.argv)

if re.search("-i[= ]", cmd):
    ubicacion, escala, filtros = params(cmd)
    print(filtros)

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
