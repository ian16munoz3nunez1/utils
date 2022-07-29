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
    if re.search(r'90', f):
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if re.search(r'180', f):
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    if re.search(r'270', f):
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    if re.search(r'x', f):
        frame = cv2.flip(frame, 0)
    if re.search(r'y', f):
        frame = cv2.flip(frame, 1)

    return frame

def parametros(cmd):
    video = None
    inicio = None
    fin = None
    filtros = None

    if re.search(r"\s-[qxy012789]+\s?", cmd):
        m = re.search(r"\s-[qxy012789]+\s?", cmd)
        if m.end() == len(cmd):
            filtros = cmd[m.start()+1:m.end()]
            cmd = re.sub(r"\s-[qxy012789]+", '', cmd)
        else:
            filtros = cmd[m.start()+1:m.end()-1]
            cmd = re.sub(r"\s-[qxy012789]+\s?", ' ', cmd)

    m = re.split(r"(\s-[iovse]+[= ])", cmd)
    m.pop(0)

    params = {}

    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    if '-i' in params.keys():
        entrada = params['-i']
    if '-o' in params.keys():
        salida = params['-o']
    if '-v' in params.keys():
        video = paras['-v']
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

    return entrada, salida, video, inicio, fin, filtros

cmd = ''.join(' ' + i for i in sys.argv)

if re.search(r"\s-i[= ]", cmd) and re.search(r"\s-o[= ]", cmd):
    entrada, salida, video, inicio, fin, filtros = parametros(cmd)
    print(Fore.CYAN + "[*] Entrada:", entrada)
    print(Fore.CYAN + "[*] Salida:", salida)
    print(Fore.CYAN + "[*] Video:", video)
    print(Fore.CYAN + "[*] Inicio:", inicio)
    print(Fore.CYAN + "[*] Fin:", fin)
    print(Fore.CYAN + "[*] Filtros:", filtros)

    if filtros:
        quality = re.search(r"q", filtros)
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

