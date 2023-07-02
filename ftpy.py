import socket
import os
import sys
import time
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

ipAddr = sys.argv[1]
host, port = "0.0.0.0", 8080
root = os.getcwd()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)

print(Fore.GREEN + f"[+] Corriendo servidor en http://{ipAddr}:{port}")
print(Fore.YELLOW + "[!] Presiona Ctrl+C para terminar el proceso")

while True:
    conexion, addr = sock.accept()
    request = conexion.recv(1024).decode()

    info = request.split(' ')

    route = info[1]
    route = route.split('?')[0]
    route = route.lstrip('/')

    if route == "favicon.ico":
        continue

    fecha = time.strftime("%d/%m/%y")
    hora = time.strftime("%H:%M:%S")
    print(Fore.CYAN + f"[*] {addr[0]} - - [{fecha} {hora}] \"{info[0]} http://{ipAddr}:{port}{info[1]}\"")
    path = f"{root}/{route.replace('%20', ' ')}"
    if os.path.isdir(path):
        title = os.path.abspath(path)
        title = os.path.basename(title)
        os.chdir(path)

        header = "HTTP/1.1 200 OK\r\n\r\n".encode()
        response = f"<html> <head> <title> {title} </title> </head>".encode()
        response += "<body> <ul>".encode()

        archivos = os.listdir(path)
        archivos.sort(key=str.lower)
        for i in archivos:
            ubicacion = f"{path}/{i}"
            if os.path.isdir(ubicacion):
                response += f"<li> <a href=\"http://{ipAddr}:{port}/{route}/{i}\"> {i}/ </a> </li>".encode()
            else:
                response += f"<li> <a href=\"http://{ipAddr}:{port}/{route}/{i}\"> {i} </a> </li>".encode()

        response += "</ul> </body>".encode()
        response += "</html>".encode()

    if os.path.isfile(path):
        archivo = open(path, 'rb')
        response = archivo.read()
        archivo.close()

        header = "HTTP/1.1 OK\r\n\r\n".encode()

    finalResponse = header + response

    conexion.send(finalResponse)
    conexion.close()

