# Ian Mu;oz Nu;ez

import cv2
import numpy
import sys
import os
import re
from random import randint
from colorama import init
from colorama.ansi import Fore
from time import sleep

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica la ubicacion de la imagen o directorio")
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

# La funcion 'escalar' escala la imagen para ser visible en la pantalla
def escalar(height, width):
    if height > width:
        escala = 600/height
    elif width > height:
        escala = 600/width
    else:
        escala = 600/height

    return escala

# La funcion 'getNombre' regresa el nombre base del archivo de imagen
def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(ubicacion)

    return nombre

# La funcion 'isImage' regresa si la ubicacion ingresada es una imagen
def isImage(ubicacion):
    ext = ['.jpg', '.png', '.jpeg', '.webp', '.JPG', '.PNG', '.JPEG', '.WEBP']

    imagen = False
    for i in ext:
        if ubicacion.endswith(i):
            imagen = True
            break

    return imagen

def isVideo(ubicacion):
    ext = ['.mp4', '.avi', '.wav']

    video = False
    for i in ext:
        if ubicacion.endswith(i):
            video = True
            break

    return video

# La funcion 'filtrar' aplica los filtros ingresados por el usuario
def filtrar(imagen, f):
    if re.search(r'90', f): # Gira la imagen 90 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search(r'180', f): # Gira la imagen 180 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_180)
    if re.search(r'270', f): # Gira la imagen -90 grados
        imagen = cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
    if re.search(r'x', f): # Gira la imagen en el eje 'x'
        imagen = cv2.flip(imagen, 0)
    if re.search(r'y', f): # Gira la imagen en el eje 'y'
        imagen = cv2.flip(imagen, 1)
    if re.search(r'g', f): # Aplica una escala de grises a la imagen
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    if re.search(r'n', f): # Cambia la imagen a su negativa
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

# La funcion 'parametros' regresa los parametros ingresados por el usuario
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

    # Regresa la ubicacion de la imagen, si se ingreso la escala deseada, y los filtros encontrados
    return ubicacion, escala, filtros

cmd = ''.join(' ' + i for i in sys.argv)

# Si se encuentra la bandera -h o --help se muestra una ayuda para el usuario
if (re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd)) and not re.search(r"\s-i[= ]", cmd):
    manual()
    exit()

# Revisa que la bandera -i se encuentre en el comando
if not re.search(r"\s-i[= ]", cmd):
    print(Fore.RED + "[+] Ubicacion de la imagen no ingresada")
    exit()

ubicacion, escala, filtros = parametros(cmd) # Se obtienen los parametros del comando

# Si la ubicacion es un directorio...
if os.path.isdir(ubicacion):
    # Se crea una lista de archivos que tengan extensiones de imagen
    archivos = []
    for i in os.listdir(ubicacion):
        archivo = f"{ubicacion}/{i}"
        if os.path.isfile(archivo) and (isImage(i) or isVideo(archivo)):
            archivos.append(archivo)

    # Si en el directorio no se encuentra ninguna imagen se termina la ejecucion del programa
    if len(archivos) == 0:
        print(Fore.YELLOW + f"[!] El directorio \"{ubicacion}\" no contiene archivos de imagen")
        exit()
    
    # Se obtiene un numero aleatorio para elegir la imagen
    numero = randint(0, len(archivos)-1)
    archivo = archivos[numero]

    if isImage(archivo):
        imagen = cv2.imread(archivo) # Se obtiene el contenido de la imagen
        height, width = imagen.shape[:2] # Se obtienen las dimensiones de la imagen
        escala = escala if escala else escalar(height, width)
        imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

        # Si se encontraron filtros en el comando se aplican
        if filtros:
            imagen = filtrar(imagen, filtros)

        # Se muestran datos de la imagen
        print(Fore.CYAN + "[*] Ubicacion:", archivo)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        # Se obtiene el nombre de la imagen y se muestra
        nombre = getNombre(archivo)
        if re.search(r"[^a-zA-Z0-9. ]", nombre):
            nombre = re.sub(r"[^a-zA-Z0-9. ]", '', nombre)
        cv2.imshow(nombre, imagen)

        # El programa espera a que se presione la tecla Esc para terminar la ejecucion
        while True:
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()

    if isVideo(archivo):
        captura = cv2.VideoCapture(archivo)
        height = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(captura.get(cv2.CAP_PROP_FPS))
        escala = escala if escala else escalar(height, width)

        # Se muestran datos de la imagen
        print(Fore.CYAN + "[*] Ubicacion:", archivo)
        print(Fore.CYAN + "[*] FPS:", fps)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        # Se obtiene el nombre de la imagen y se muestra
        nombre = getNombre(archivo)
        if re.search(r"[^a-zA-Z0-9. ]", nombre):
            nombre = re.sub(r"[^a-zA-Z0-9. ]", '', nombre)

        while True:
            leido, video = captura.read()

            if not leido:
                break
            if cv2.waitKey(1) == 27:
                break

            if filtros:
                video = filtrar(video, filtros)
            video = cv2.resize(video, None, fx=escala, fy=escala)

            cv2.imshow(nombre, video)
            sleep(1/fps)
        cv2.destroyAllWindows()

# Si la ubicacion es un archivo y tiene una extension de imagen...
elif os.path.isfile(ubicacion) and (isImage(ubicacion) or isVideo(ubicacion)):
    if isImage(ubicacion):
        imagen = cv2.imread(ubicacion) # Se lee el contenido de la imagen
        height, width = imagen.shape[:2] # Se obtienen las dimensiones de la imagen
        escala = escala if escala else escalar(height, width)
        imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

        # Si se encontraron filtros en el comando se aplican
        if filtros:
            imagen = filtrar(imagen, filtros)

        # Se muestran datos de la imagen
        print(Fore.CYAN + "[*] Ubicacion:", ubicacion)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        # Se obtiene el nombre de la imagen y se muestra
        nombre = getNombre(ubicacion)
        if re.search(r"[^a-zA-Z0-9. ]", nombre):
            nombre = re.sub(r"[^a-zA-Z0-9. ]", '', nombre)
        cv2.imshow(nombre, imagen)

        # El programa espera a que se presione la tecla Esc para terminar la ejecucion
        while True:
            if cv2.waitKey(1) == 27:
                break
        cv2.destroyAllWindows()

    if isVideo(ubicacion):
        captura = cv2.VideoCapture(ubicacion)
        height = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = int(captura.get(cv2.CAP_PROP_FPS))
        escala = escala if escala else escalar(height, width)

        # Se muestran datos de la imagen
        print(Fore.CYAN + "[*] Ubicacion:", ubicacion)
        print(Fore.CYAN + "[*] FPS:", fps)
        print(Fore.CYAN + "[*] Escala:", escala)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)

        # Se obtiene el nombre de la imagen y se muestra
        nombre = getNombre(ubicacion)
        if re.search(r"[^a-zA-Z0-9. ]", nombre):
            nombre = re.sub(r"[^a-zA-Z0-9. ]", '', nombre)

        while True:
            leido, video = captura.read()

            if not leido:
                break
            if cv2.waitKey(1) == 27:
                break

            if filtros:
                video = filtrar(video, filtros)
            video = cv2.resize(video, None, fx=escala, fy=escala)

            cv2.imshow(nombre, video)
            sleep(1/fps)
        cv2.destroyAllWindows()

else:
    print(Fore.RED + f"[-] Ubicacion \"{ubicacion}\" no encontrada o incompatible")

