import sys
import cv2 as cv
import socket
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def manual():
    print(Fore.YELLOW + "arg1: Camara a usar (valor entero)")
    print(Fore.YELLOW + "arg2: Puerto a usar (valor entero)")

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    manual()
    exit()

host = '0.0.0.0'
cam, port = int(sys.argv[1]), int(sys.argv[2])
captura = cv.VideoCapture(cam)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((host, port))
sock.listen(1)
print(Fore.CYAN + "[*] Esperando conexion...")

while True:
    try:
        conexion, addr = sock.accept()
        request = conexion.recv(1024)

        leido, frame = captura.read()

        if not leido:
            break

        if cv.waitKey(1) == 27:
            break

        frame = cv.imencode('.jpg', frame)[1]
        frame = bytearray(frame)
        header = 'HTTP/1.1 200 OK\r\n\r\n'.encode()
        response = header + frame
        conexion.send(response)

        conexion.close()

    except KeyboardInterrupt:
        break

sock.close()
captura.release()
print(Fore.YELLOW + "[!] Transmision terminada")

