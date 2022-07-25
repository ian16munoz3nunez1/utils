import cv2
import os
import sys
import re
from colorama import init
from colorama.ansi import Fore
from time import sleep

init(autoreset=True)

def escalar(height, width):
    escala = (height+width)/2
    escala = 700/escala

    return escala

def isVideo(ubicacion):
    ext = [".mp4", ".mov", ".avi", ".flv", ".wmv"]
    extUpper = [i.upper() for i in ext]

    video = False
    i = 0
    while i < len(ext):
        if ubicacion.endswith(ext[i]):
            video = True
            break
        if ubicacion.endswith(exUpper[i]):
            video = True
            break
        i += 1

    return video

def filtrar(frame, f):
    if re.search('90', f):
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search('180', f):
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    if re.search('270', f):
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if re.search('x', f):
        frame = cv2.flip(frame, 0)
    if re.search('y', f):
        frame = cv2.flip(frame, 1)

    return frame

def params(cmd):
    entrada = None
    salida = None
    video = None
    inicio = None
    fin = None
    filtros = None

    try:
        entrada = re.findall("-i[= ]([\W\w]+) -[ovseqxy012789]+", cmd)[0]
    except:
        entrada = re.findall("-i[= ]([\W\w]+)", cmd)[0]

    try:
        salida = re.findall("-o[= ]([\W\w]+) -[ivseqxy012789]+", cmd)[0]
    except:
        salida = re.findall("-o[= ]([\W\w]+)", cmd)[0]

    if re.search("-v[= ]", cmd):
        try:
            video = re.findall("-v[= ]([\W\w]+) -[ioseqxy012789]+", cmd)[0]
        except:
            video = re.findall("-v[= ]([\W\w]+)", cmd)[0]

    if re.search("-s[= ]", cmd):
        try:
            inicio = int(re.findall("-s[= ]([0-9]+) -[ioveqxy012789]+", cmd)[0])
        except:
            inicio = int(re.findall("-s[= ]([0-9]+)", cmd)[0])

    if re.search("-e[= ]", cmd):
        try:
            fin = int(re.findall("-e[= ]([0-9]+) -[iovsqxy012789]+", cmd)[0])
        except:
            fin = int(re.findall("-e[= ]([0-9]+)", cmd)[0])

    if re.search("-[qxy012789]+", cmd):
        try:
            filtros = re.findall("-([qxy012789]+) -[iovse]+", cmd)[0]
        except:
            filtros = re.findall("-([qxy012789]+)", cmd)[0]

    return entrada, salida, video, inicio, fin, filtros

cmd = ''.join(' ' + i for i in sys.argv)

if re.search("-i[= ]", cmd) and re.search("-o[= ]", cmd):
    entrada, salida, video, inicio, fin, filtros = params(cmd)

    if filtros:
        quality = re.search("q", filtros)
    else:
        quality = None
    if not quality and video:
        print(Fore.YELLOW + "[!] La calidad del video y sus dimensiones pueden causar un conflicto")
        exit()
    if salida == entrada or video == entrada:
        print(Fore.YELLOW + "[!] Salida o video igual a entrada\nPuede ser peligroso...")
        exit()

    if os.path.isfile(entrada) and isVideo(entrada):
        if not os.path.isdir(salida):
            os.mkdir(salida)

        print(Fore.YELLOW + "[!] Mostrar video?...\n[S/n]", end=' ')
        show = input()
        if len(show) == 0 or show.upper() == 'S':
            show = 'S'

        if inicio is None:
            inicio = 0

        captura = cv2.VideoCapture(entrada)
        height = int(captura.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(captura.get(cv2.CAP_PROP_FRAME_WIDTH))
        if not quality:
            escala = escalar(height, width)
        else:
            escala = 1
        fps = int(captura.get(cv2.CAP_PROP_FPS))

        print(Fore.CYAN + "[*] Frames:", captura.get(cv2.CAP_PROP_FRAME_COUNT))
        print(Fore.CYAN + "[*] Frame inicial:", inicio*fps)
        print(Fore.CYAN + "[*] Height:", height)
        print(Fore.CYAN + "[*] Width:", width)
        print(Fore.CYAN + "[*] FPS:", fps)
        print(Fore.CYAN + "[*] Escala:", escala)

        if video:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            output = cv2.VideoWriter(video, fourcc, fps, (width, height))
            print(Fore.CYAN + "[*] Nombre:", video)

        captura.set(cv2.CAP_PROP_POS_FRAMES, inicio*fps)
        i = inicio*fps
        while True:
            leido, frame = captura.read()

            if not leido:
                break

            if cv2.waitKey(1) == 27:
                break

            if fin and i == fin*fps:
                break

            if not quality:
                frame = cv2.resize(frame, None, fx=escala, fy=escala)

            if filtros:
                frame = filtrar(frame, filtros)

            if video or show == 'S':
                cv2.imshow(entrada, frame)
            else:
                print(f"Frame: {i}", end='\r')

            cv2.imwrite(f"{salida}/{salida}{i}.jpg", frame)
            if video:
                output.write(frame)

            i += 1

        captura.release()
        cv2.destroyAllWindows()

    else:
        print(Fore.RED + f"[-] Archivo \"{entrada}\" no encontrado o no es compatible")

else:
    print(Fore.RED + "[-] error de sintaxis")

