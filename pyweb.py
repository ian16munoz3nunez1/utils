# Ian Mu;oz Nu;ez

import cv2
import numpy
import sys
import re
import requests
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -u" + Fore.RED + " --> " + Fore.WHITE + "Especifica la URL de la imagen")
    print(Fore.GREEN + "+ -t" + Fore.RED + " --> " + Fore.WHITE + "Especifica la escala con la que se mostrara la imagen")
    print(Fore.GREEN + "+ -90" + Fore.RED + " --> " + Fore.WHITE + "Gira la imagen 90 grados")
    print(Fore.GREEN + "+ -180" + Fore.RED + " --> " + Fore.WHITE + "Gira la imagen 180 grados")
    print(Fore.GREEN + "+ -270" + Fore.RED + " --> " + Fore.WHITE + "Gira la imagen 270 grados")
    print(Fore.GREEN + "+ -x" + Fore.RED + " --> " + Fore.WHITE + "Gira la imagen sobre el eje 'x'")
    print(Fore.GREEN + "+ -y" + Fore.RED + " --> " + Fore.WHITE + "Gira la imagen sobre el eje 'y'")
    print(Fore.GREEN + "+ -g" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen en escala de grises")
    print(Fore.GREEN + "+ -n" + Fore.RED + " --> " + Fore.WHITE + "Muestra la negativa de la imagen")
    print(Fore.GREEN + "+ -m" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen en espejo")
    print(Fore.GREEN + "+ -c" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen con el filtro de Canny")
    print(Fore.GREEN + "+ -h" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen con el filtro de Harris")
    print(Fore.GREEN + "+ -s" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen como un sketch")

# La funcion 'escalar' escala la imagen a la pantalla para ser completamente visible
def escalar(height, width):
    if height > width:
        escala = 600/height
    elif width > height:
        escala = 600/width
    else:
        escala = 600/height

    return escala

# La funcion 'getExt' regresa si la URL es valida y la extension del archivo de esta URL
def getExt(url):
    extensiones = ["jpg", "png", "jpeg", "webp"]
    extensionesUpper = [i.upper() for i in extensiones]

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

# La funcion 'filtar' aplica los filtros ingresados por el usuario
def filtrar(imagen, f):
    if re.search(r'90', f): # Gira la imagen 90 gradps
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search(r'180', f): # Gira la imagen 180 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_180)
    if re.search(r'270', f): # Gira la imagen -90 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    if re.search(r'x', f): # Gira la imagen en el eje 'x'
        imagen = cv2.flip(imagen, 0)
    if re.search(r'y', f): # Gira la imagen en el eje 'y'
        imagen = cv2.flip(imagen, 1)
    if re.search(r'g', f): # Muestra la imagen en escala de grises
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    if re.search(r'n', f): # Muestra la negativa de la imagen
        imagen = 255 - imagen
    if re.search(r'm', f): # Aplica un filtro de espejo a la imagen
        flip = cv2.flip(imagen, 1)
        imagen = numpy.hstack((imagen, flip))
    if re.search(r'c', f): # Aplica el filtro de 'Canny' a la imagen
        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (3,3), 0)
        t1 = int(input("Threshold1: "))
        t2 = int(input("Threshold2: "))
        canny = cv2.Canny(image=blur, threshold1=t1, threshold2=t2)
        imagen = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    if re.search(r'h', f): # Aplica el filtro de 'Harris' a la imagen
        v = float(input("Valor de Harris: "))
        back = input("Fondo negro [S/n]> ")
        dil = input("Dilatar [S/n]> ")
        col = input("Color (red/green/blue/yellow/magenta/cyan): ")
        if col.lower() == "red" or col.lower() == "rojo":
            color = [0, 0, 255]
        elif col.lower() == "green" or col.lower() == "verde":
            color = [0, 255, 0];
        elif col.lower() == "blue" or col.lower() == "azul":
            color = [255, 0, 0]
        elif col.lower() == "yellow" or col.lower() == "amarillo":
            color = [0, 255, 255]
        elif col.lower() == "magenta":
            color = [255, 0, 255]
        elif col.lower() == "cyan" or col.lower() == "cian":
            color = [255, 255, 0]
        else:
            color = [255, 255, 255]

        grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        grises = numpy.float32(grises)
        harris = cv2.cornerHarris(grises, 2, 3, 0.04)
        if len(dil) == 0 or dil.upper() == 'S' or dil.upper()[0] == 'S':
            harris = cv2.dilate(harris, None)

        imagen[harris > v*harris.max()] = color
        if len(back) == 0 or back.upper() == 'S' or back.upper()[0] == 'S':
            imagen[harris < v*harris.max()] = [0, 0, 0]
    if re.search(r's', f): # Aplica un filtro de sketch a la imagen
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(invert, (49, 49), 0)
        invertBlur = cv2.bitwise_not(blur)
        imagen = cv2.divide(gray, invertBlur, scale=256.0)


    return imagen # Regresa la imagen con los filtros aplicados

# La funcion 'parametros regresa los parametros ingresados por el usuario
def parametros(cmd):
    escala = None
    filtros = None

    if re.search(r"\s-[xygnmchs012789]+\s?", cmd):
        m = re.search(r"\s-[xygnmchs012789]+\s?", cmd)
        if m.end() == len(cmd):
            filtros = cmd[m.start()+1:m.end()]
            cmd = re.sub(r"\s-[xygnmchs012789]+", '', cmd)
        else:
            filtros = cmd[m.start()+1:m.end()-1]
            cmd = re.sub(r"\s-[xygnmchs012789]+\s?", ' ', cmd)

    m = re.split(r"(\s-[tu]+[= ])", cmd)
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

# Si se encuentra la bandera -h o --help se muestra ayuda para el usuario
if (re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd)) and not re.search(r"\s-u[= ]", cmd):
    manual()
    exit()

# Se revisa que la bandera -u se encuentre en el comando
if not re.search(r"\s-u[= ]", cmd):
    print(Fore.RED + "[-] Direccion URL no ingresada")
    exit()

url, escala, filtros = parametros(cmd) # Se obtienen los parametros ingresados por el usuario
valido, extension = getExt(url)

if valido:
    nombre = re.findall(f"/([\W\w]+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]

    req = requests.get(url)
    matriz = numpy.frombuffer(req.content, dtype=numpy.uint8)

    original = cv2.imdecode(matriz, -1)
    height, width = original.shape[:2]

    escala = escala if escala else escalar(height, width)
    imagen = cv2.resize(original, None, fx=escala, fy=escala)

    if filtros:
        imagen = filtrar(imagen, filtros)

    print(Fore.CYAN + "[*] Nombre:", nombre)
    print(Fore.CYAN + "[*] Escala:", escala)
    cv2.imshow(nombre, imagen)
    while True:
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == ord('s'):
            cv2.imwrite(nombre, original)
            print(Fore.GREEN + f"[+] Imagen \'{nombre}\' guardada")
            break
    cv2.destroyAllWindows()

else:
    print("error")

