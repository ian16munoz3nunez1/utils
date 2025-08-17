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
    print(Fore.YELLOW + "arg1: Camara a utilizar (int)")
    print(Fore.YELLOW + "arg2: Puerto a utilizar (int)")

if sys.argv[1] == '--help' or sys.argv[1] == '-h':
    manual()
    exit()

try:
    cam, port = int(sys.argv[1]), int(sys.argv[2])
except:
    manual()
    exit()

addr = ('0.0.0.0', port)
chunk = 4*1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind(addr)

try:
    while True:
        capture = cv.VideoCapture(cam)
        sock.listen(1)
        client, _ = sock.accept()

        try:
            while True:
                read, frame = capture.read()

                if not read:
                    break

                data = pickle.dumps(frame)
                client.sendall(struct.pack('Q', len(data)))
                client.sendall(data)

            client.close()
            print("Client disconnected")

        except Exception as e:
            client.close()
            capture.release()
            print(f"An error has ocurred: {e}")

except KeyboardInterrupt as e:
    print(f"Keyboard interrupt")

finally:
    sock.close()

