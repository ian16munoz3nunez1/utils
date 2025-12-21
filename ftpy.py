#!python3

# Ian Mu;oz Nu;ez

import socket
import os
import time
from subprocess import Popen, PIPE
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)


def getHTML(path, path_type):
    if path_type == 'dir':
        title = os.path.abspath(path)
        title = os.path.basename(title)
        os.chdir(path)

        header = "HTTP/1.1 200 OK\r\n\r\n".encode()
        response = f"<html> <head> <title> {title} </title> </head>".encode()
        response += "<meta charset=\"utf-8\">".encode()
        response += "<body> <ul>".encode()
        if route != '':
            response += f"<li> <a href=\"{os.path.dirname('/' + route.rstrip('/'))}\"> ../ </a> </li>".encode()

        archivos = os.listdir(path)
        archivos.sort(key=str.lower)
        for i in archivos:
            ubicacion = os.path.join(path, i)
            url = f"{route}/{i}".lstrip('/')
            if os.path.isdir(ubicacion):
                response += f"<li> <a href=\"http://{ipAddr}:{port}/{url}\"> {i}/ </a> </li>".encode()
            else:
                response += f"<li> <a href=\"http://{ipAddr}:{port}/{url}\"> {i} </a> </li>".encode()

        response += "</ul> </body>".encode()
        response += "</html>".encode()

    if path_type == 'file':
        if path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
            content_type = 'image/jpeg'
        elif path.lower().endswith('.png'):
            content_type = 'image/png'
        elif path.lower().endswith('.webp'):
            content_type = 'image/webp'
        else:
            content_type = 'text/plain'

        archivo = open(path, 'rb')
        response = archivo.read()
        archivo.close()

        header = "HTTP/1.1 200 OK\r\n" \
                 f"Content-Type: {content_type}\r\n" \
                 f"Content-Length: {len(response)}\r\n" \
                 f"Connection: close\r\n\r\n".encode()

    return header + response

result = Popen(r"ifconfig wlan0 | grep -m1 inet | sed -r 's/\s+/,/g' | cut -d, -f3", shell=PIPE, stdin=PIPE, stdout=PIPE, stderr=PIPE)
ipAddr = (result.stdout.read() + result.stderr.read()).decode().replace('\n', '')
host, port = "0.0.0.0", 8080
root = os.getcwd()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)

print(Fore.GREEN + f"[+] Corriendo servidor en http://{ipAddr}:{port}")
print(Fore.YELLOW + "[!] Presiona Ctrl+C para terminar el proceso")

while True:
    try:
        conexion, addr = sock.accept()

    except KeyboardInterrupt:
        print("Finishing server...")
        break

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

    path = os.path.join(root, route.replace('%20', ' '))
    if os.path.isdir(path):
        finalResponse = getHTML(path, 'dir')

    if os.path.isfile(path):
        finalResponse = getHTML(path, 'file')

    try:
        conexion.sendall(finalResponse)
        conexion.close()

    except Exception:
        conexion.close()
