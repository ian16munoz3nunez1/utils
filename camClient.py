#!python3

import sys
import cv2 as cv
import socket
import pickle
import struct
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def manual():
    print(Fore.YELLOW + "arg1: IP a conectarse (string)")
    print(Fore.YELLOW + "arg2: Puerto a utilizar")

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    manual()
    exit()

try:
    host, port = sys.argv[1], int(sys.argv[2])

except:
    manual()
    exit()

addr = (host, port)
chunk = 4*1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.connect(addr)
except:
    print(f"Unable to connect to {addr[0]} through {addr[1]}")
    exit()

data = b''
size = struct.calcsize('Q')

while True:
    while len(data) < size:
        packet = sock.recv(chunk)
        if not packet:
            break
        data += packet

    if not data:
        break

    dataSize = data[:size]
    data = data[size:]
    byteSize = struct.unpack('Q', dataSize)[0]

    while len(data) < byteSize:
        data += sock.recv(chunk)

    frame = data[:byteSize]
    data = data[byteSize:]
    frame = pickle.loads(frame)

    cv.imshow("Video", frame)
    if cv.waitKey(1) == 27:
        break

sock.close()
cv.destroyAllWindows()

