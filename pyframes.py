#!python3

# Ian Mu;oz Nu;ez

import cv2
import numpy
import os
import sys
import re
from colorama import init
from colorama.ansi import Fore
from time import sleep

init(autoreset=True)

# La funcion 'manual' muestra ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -i" + Fore.RED + " --> " + Fore.WHITE + "Especifica la ubicacion del video")
    print(Fore.YELLOW + "* -o" + Fore.RED + " --> " + Fore.WHITE + "Especifica el nombre del directorio de salida")
    print(Fore.GREEN + "+ -s" + Fore.RED + " --> " + Fore.WHITE + "Especifica el segundo en el que se quiere iniciar a procesar el video")
    print(Fore.GREEN + "+ -e" + Fore.RED + " --> " + Fore.WHITE + "Especifica el segundo en el que se quieres terminar de procesar el video")
    print(Fore.GREEN + "+ -q" + Fore.RED + " --> " + Fore.WHITE + "Mantiene la calidad original del video")
    print(Fore.GREEN + "+ -90" + Fore.RED + " --> " + Fore.WHITE + "Gira el video 90 grados")
    print(Fore.GREEN + "+ -180" + Fore.RED + " --> " + Fore.WHITE + "Gira el video 180 grados")
    print(Fore.GREEN + "+ -270" + Fore.RED + " --> " + Fore.WHITE + "Gira el video -90 grados")
    print(Fore.GREEN + "+ -x" + Fore.RED + " --> " + Fore.WHITE + "Gira el video en el eje 'x'")
    print(Fore.GREEN + "+ -y" + Fore.RED + " --> " + Fore.WHITE + "Gire el video en el eje 'y'")
    print(Fore.GREEN + "+ -g" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen en escala de grises")
    print(Fore.GREEN + "+ -n" + Fore.RED + " --> " + Fore.WHITE + "Muestra la negativa de la imagen")
    print(Fore.GREEN + "+ -m" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen en espejo")
    print(Fore.GREEN + "+ -c" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen con el filtro de Canny")
    print(Fore.GREEN + "+ -h" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen con el filtro de Harris")
    print(Fore.GREEN + "+ -k" + Fore.RED + " --> " + Fore.WHITE + "Muestra la imagen como un sketch")

# La funcion 'escalar' obtiene la imagen para adaptar la imagen a la pantalla
def escalar(height, width):
    if height < width:
        escala = 600/height
    elif width > height:
        escala = 600/width
    else:
        escala = (height+width)/2
        escala = 600/escala

    return escala

# La funcion 'isVideo' regresa si la ubicacion ingresada es un video o no
def isVideo(ubicacion):
    ext = [".mp4", ".mov", ".avi", ".flv", ".wmv"]
    extUpper = [i.upper() for i in ext]

    video = False
    i = 0
    while i < len(ext):
        if ubicacion.endswith(ext[i]):
            video = True
            break
        if ubicacion.endswith(extUpper[i]):
            video = True
            break
        i += 1

    return video

# La funcion 'filtrar' aplica los filtros ingresados por el usuario
def filtrar(frame, f, t1=None, t2=None, v=None, back=None, dil=None, col=None):
    if re.search(r'90', f): # Gira la imagen 90 grados
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search(r'180', f): # Gira la imagen 180 grados
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    if re.search(r'270', f): # Gira la imagen -90 grados
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if re.search(r'x', f): # Gira la imagen en el eje 'x'
        frame = cv2.flip(frame, 0)
    if re.search(r'y', f): # Gira la imagen en el eje 'y'
        frame = cv2.flip(frame, 1)
    if re.search(r'g', f): # Aplica una escala de grises a la imagen
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if re.search(r'n', f): # Cambia la imagen a su negativa
        frame = 255 - frame
    if re.search(r'm', f): # Aplica un filtro de espejo a la imagen
        flip = cv2.flip(frame, 1)
        frame = numpy.hstack((frame, flip))
    if re.search(r'c', f): # Aplica el filtro de 'Canny' a la imagen
        if t1 == None or t2 == None:
            t1 = 10
            t2 = 200
        grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grises, (3,3), 0)
        canny = cv2.Canny(image=blur, threshold1=t1, threshold2=t2)
        frame = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
    if re.search(r'h', f): # Aplica el filtro de 'Harris' a la imagen
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

        grises = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grises = numpy.float32(grises)
        harris = cv2.cornerHarris(grises, 2, 3, 0.04)
        if len(dil) == 0 or dil.upper() == 'S' or dil.upper()[0] == 'S':
            harris = cv2.dilate(harris, None)

        frame[harris > v*harris.max()] = color
        if len(back) == 0 or back.upper() == 'S' or back.upper()[0] == 'S':
            frame[harris < v*harris.max()] = [0, 0, 0]
    if re.search(r'k', f): # Aplica un filtro de sketch a la imagen
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(gray)
        blur = cv2.GaussianBlur(invert, (49, 49), 0)
        invertBlur = cv2.bitwise_not(blur)
        frame = cv2.divide(gray, invertBlur, scale=256.0)

    return frame

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    inicio = None
    fin = None
    filtros = None

    # Se encuentran las banderas de filtros en el comando y se eliminan
    if re.search(r"\s-[qxygnmchk012789]+\s?", cmd):
        m = re.search(r"\s-[qxygnmchk012789]+\s?", cmd)
        if m.end() == len(cmd):
            filtros = cmd[m.start()+1:m.end()]
            cmd = re.sub(r"\s-[qxygnmchk012789]+", '', cmd)
        else:
            filtros = cmd[m.start()+1:m.end()-1]
            cmd = re.sub(r"\s-[qxygnmchk012789]+\s?", ' ', cmd)

    # Se separan las banderas con parametros en un arreglo
    m = re.split(r"(\s-[iose]+[= ])", cmd)
    m.pop(0)

    # Se hace un diccionario con las banderas y valores del arreglo antes creado
    params = {}
    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    entrada = params['-i']
    salida = params['-o']
    if '-s' in params.keys():
        try:
            inicio = int(params['-s'])
        except:
            pass
    if '-e' in params.keys():
        try:
            fin = int(params['-e'])
        except:
            pass

    return entrada, salida, inicio, fin, filtros

cmd = ''.join(' ' + i for i in sys.argv)

# Si se encuentra la bandera -h o --help se muestra una ayuda para el usuario
if (re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd)) and not re.search(r"\s-i[= ]", cmd):
    manual()
    exit()

# Se revisa que la bandera -i se encuentre en el comando
if not re.search(r"\s-i[= ]", cmd):
    print(Fore.RED + "[-] Ubicacion del video no ingresada")
    exit()

# Se revisa que la bandera -o se encuentre en el comando
if not re.search(r"\s-o[= ]", cmd):
    print(Fore.RED + "[-] Directorio de salida no especificado")
    exit()

# Se obtienen los parametros ingresados y se muestran los datos obtenidos de estos
entrada, salida, inicio, fin, filtros = parametros(cmd)

# Se revisa si la ubicacion ingresada es un video
if os.path.isfile(entrada) and not isVideo(entrada):
    print(Fore.RED + f"[-] Video \"{entrada}\" no encontrado o no es compatible")
    exit()

# Si la entrada es igual a la salida se cancela el proceso
if salida == entrada:
    print(Fore.YELLOW + "[!] La salida es igual a la entrada\nPueden sobreescribirse los datos...")
    exit()

print(Fore.CYAN + "[*] Entrada:", entrada)
print(Fore.CYAN + "[*] Salida:", salida)
print(Fore.CYAN + "[*] Inicio:", inicio)
print(Fore.CYAN + "[*] Fin:", fin)
print(Fore.CYAN + "[*] Filtros:", filtros)

# Si el directorio de salida no existe, se crea uno nuevo
if not os.path.isdir(salida):
    os.mkdir(salida)

inicio = 0 if inicio is None else inicio # Si no se ingreso ningun punto de inicio para el video, se establece en 0

# Si el filtro 'q' se encuentra en el comando, se mantiene la calidad del video
if filtros:
    t1 = None
    t2 = None
    v = None
    back = None
    dil = None
    col = None

    quality = re.search(r"q", filtros)
    if re.search(r'c', filtros):
        t1 = int(input("Threshold1: "))
        t2 = int(input("Threshold2: "))

    if re.search(r'h', filtros):
        v = float(input("Valor de Harris: "))
        back = input("Fondo negro [S/n]> ")
        dil = input("Dilatar [S/n]> ")
        col = input("Color: ")

else:
    quality = None

print(Fore.MAGENTA + "[?] Mostrar video?...\n[S/n]", end=' ')
show = input()
if len(show) == 0 or show.upper()[0] == 'S':
    show = True
else:
    show = False

# Se inicia la captura y los valores para guardar los frames
captura = cv2.VideoCapture(entrada)
height = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
if quality:
    escala = 1
else:
    escala = escalar(height, width)
fps = int(captura.get(cv2.CAP_PROP_FPS))

print(Fore.CYAN + "[*] Frames:", captura.get(cv2.CAP_PROP_FRAME_COUNT))
print(Fore.CYAN + "[*] Frame inicial:", inicio*fps)
print(Fore.CYAN + "[*] Height:", height)
print(Fore.CYAN + "[*] Width:", width)
print(Fore.CYAN + "[*] FPS:", fps)
print(Fore.CYAN + "[*] Escala:", escala)

print(Fore.MAGENTA + "[?] Iniciar proceso?...\n[S/n]", end=' ')
continuar = input()
if len(continuar) == 0 or continuar.upper() == 'S' or continuar.upper()[0] == 'S':
    pass
else:
    print(Fore.YELLOW + "[!] Proceso cancelado...")
    captura.release() # Si libera la captura del video
    os.rmdir(salida)
    exit()

# Se modifica el nombre de la ubicacion para mostrar en la ventana del video
if re.search(r"[^a-zA-Z0-9. ]", entrada):
    entrada = re.sub(r"[^a-zA-Z0-9. ]", '', entrada)

captura.set(cv2.CAP_PROP_POS_FRAMES, inicio*fps) # Se inicia el video en el segundo deseado
i = inicio*fps
while True:
    leido, frame = captura.read() # Se lee lo que obtiene la captura del video

    if not leido: # Si no se lee nada se termina el ciclo
        break

    if cv2.waitKey(1) == 27: # Si se presiona la teclas Esc se termina el ciclo
        break

    if fin and i == fin*fps: # Si se llega al ultimo segundo deseado se termina el ciclo
        break

    if not quality: # Si no se ingreso la bandera -q se escala el video
        frame = cv2.resize(frame, None, fx=escala, fy=escala)

    if filtros: # Se aplican los filtros al video
        frame = filtrar(frame, filtros, t1, t2, v, back, dil, col)

    # Se muestra el video o el frame actual
    if show:
        cv2.imshow(entrada, frame)
    else:
        print(f"Frame: {i}", end='\r')

    cv2.imwrite(f"{salida}/{salida}{i}.jpg", frame)

    i += 1

captura.release()
cv2.destroyAllWindows()

