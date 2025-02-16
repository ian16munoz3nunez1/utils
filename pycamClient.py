#!python3

import sys
import cv2 as cv
from time import sleep
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def manual():
    print(Fore.YELLOW + "arg1: URL a conectarse (string)")

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    manual()
    exit()

url = sys.argv[1]
captura = cv.VideoCapture(url)

winName = 'Video'
cv.namedWindow(winName, cv.WINDOW_AUTOSIZE)

while True:
    try:
        captura.open(url)
        leido, frame = captura.read()

        if not leido:
            break

        if cv.waitKey(1) == 27:
            break

        cv.imshow(winName, frame)
        sleep(1/30)

    except:
        pass

captura.release()
cv.destroyAllWindows()
print(Fore.YELLOW + "[!] Fin de la transmision")

