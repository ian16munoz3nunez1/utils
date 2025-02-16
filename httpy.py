#!python3

# Ian Mu;oz Nu;ez

from flask import Flask, send_from_directory
import os
import sys
import re
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

# La funcion 'manual' muestra una ayuda para el usuario
def manual():
    print(Fore.YELLOW + "* -p" + Fore.RED + " --> " + Fore.WHITE + "Especifica el puerto de conexion para el servidor")
    print(Fore.GREEN + "+ -d" + Fore.RED + " --> " + Fore.WHITE + "Comparte un directorio distinto al actual")
    print(Fore.GREEN + "+ -s" + Fore.RED + " --> " + Fore.WHITE + "Muestra de forma grafica los elementos")

# La funcion 'getNombre' regresa el nombre de un archivo o directorio
def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(nombre)
    return nombre

# La funcion 'getResponseFile' regresa etiquetas html dependiendo de la ubicacion recibida
def getResponseFile(ubicacion):
    href = ubicacion.replace(' ', '%20')
    if isImage(ubicacion): # Regresa una etiqueta html de imagen
        return f"<img src=\"{ubicacion}\"></img>"
    elif isVideo(ubicacion): # Regresa una etiqueta html de video
        return f"<video src=\"{ubicacion}\" preload=\"none\" controls loop></video>"
    elif isAudio(ubicacion): # Regresa una etiqueta html de audio
        return f"<audio src=\"{ubicacion}\" controls></audio>"

    # Se regresan etiquetas 'href' con distintas imagenes dependiendo del archivo presentado
    elif ubicacion.endswith(".ino"):
        return f"<a href={href}> <img src=\".httpServer/arduino.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".c"):
        return f"<a href={href}> <img src=\".httpServer/c.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".cpp"):
        return f"<a href={href}> <img src=\".httpServer/cpp.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".cs"):
        return f"<a href={href}> <img src=\".httpServer/csharp.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".css"):
        return f"<a href={href}> <img src=\".httpServer/css.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif os.path.isdir(f"{directorio}/{ubicacion}"):
        return f"<a href=\'\'> <img src=\".httpServer/dir.png\"></img> <br>  <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".ods") or ubicacion.endswith(".xlsx"):
        return f"<a href={href}> <img src=\".httpServer/excel.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".xcf"):
        return f"<a href={href}> <img src=\".httpServer/gimp.webp\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".go"):
        return f"<a href={href}> <img src=\".httpServer/golang.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".html"):
        return f"<a href={href}> <img src=\".httpServer/html.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".java") or ubicacion.endswith(".class") or ubicacion.endswith(".jar"):
        return f"<a href={href}> <img src=\".httpServer/java.jpg\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".js"):
        return f"<a href={href}> <img src=\".httpServer/js.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".lat"):
        return f"<a href={href}> <img src=\".httpServer/latino.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".m"):
        return f"<a href={href}> <img src=\".httpServer/octave.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".pdf"):
        return f"<a href={href}> <img src=\".httpServer/pdf.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".pl"):
        return f"<a href={href}> <img src=\".httpServer/perl.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".php"):
        return f"<a href={href}> <img src=\".httpServer/php.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".odp") or ubicacion.endswith(".pptx"):
        return f"<a href={href}> <img src=\".httpServer/powerpoint.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".p"):
        return f"<a href={href}> <img src=\".httpServer/prolog.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".py"):
        return f"<a href={href}> <img src=\".httpServer/python.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".rb"):
        return f"<a href={href}> <img src=\".httpServer/ruby.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".sql"):
        return f"<a href={href}> <img src=\".httpServer/sql.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".txt") or ubicacion.endswith(".dat"):
        return f"<a href={href}> <img src=\".httpServer/txt.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".odt") or ubicacion.endswith(".docx"):
        return f"<a href={href}> <img src=\".httpServer/word.png\"></img> <br> <b>{ubicacion}</b> </a>"
    else:
        return f"<a href={href}> <img src=\".httpServer/file.png\"></img> <br> <b>{ubicacion}</b> </a>"

# Regresa si una ubicacion es una imagen o no
def isImage(ubicacion):
    ext = [".jpg", ".png", ".jpeg", ".webp", ".gif"]
    extUpper = [i.upper() for i in ext]

    imagen = False
    i = 0
    while i < len(ext):
        if ubicacion.endswith(ext[i]) or ubicacion.endswith(extUpper[i]):
            imagen = True
            break
        i += 1
    return imagen

# Regresa su una ubicacion es un video o no
def isVideo(ubicacion):
    ext = [".mp4", ".avi", ".mkv", ".webm"]
    extUpper = [i.upper() for i in ext]

    video = False
    i = 0
    while i < len(ext):
        if ubicacion.endswith(ext[i]) or ubicacion.endswith(extUpper[i]):
            video = True
            break
        i += 1
    return video

# Regresa si una ubicacion es un audio o no
def isAudio(ubicacion):
    ext = [".mp3", ".mpga", ".wav", ".opus"]
    extUpper = [i.upper() for i in ext]

    audio = False
    i = 0
    while i < len(ext):
        if ubicacion.endswith(ext[i]) or ubicacion.endswith(extUpper[i]):
            audio = True
            break
        i += 1
    return audio

# La funcion 'parametros' regresa los parametros ingresados por el usuario
def parametros(cmd):
    directorio = os.getcwd() + '/'
    show = False

    if re.search(r"\s-s\s?", cmd):
        show = True
        m = re.search(r"\s-s\s?", cmd)
        if m.end() == len(cmd):
            cmd = re.sub(r"\s-s", '', cmd)
        else:
            cmd = re.sub(r"\s-s\s?", ' ', cmd)

    m = re.split(r"(\s-[dp]+[= ])", cmd)
    m.pop(0)

    params = {}
    i = 0
    while i < len(m):
        flag = m[i].replace(' ', '')
        flag = flag.replace('=', '')
        params[flag] = m[i+1]
        i += 2

    if '-d' in params.keys():
        directorio += params['-d']
    puerto = params['-p']

    return directorio, puerto, show

cmd = ''.join(' ' + i for i in sys.argv) # Se obtiene el comando ingresado

if re.search(r"\s-+h\s?", cmd) or re.search(r"\s--help\s?", cmd):
    manual()
    exit()

# Se revisa que la bandera -p se encuentre en el comando
if not re.search(r"\s-p[= ]", cmd):
    print(Fore.RED + "[-] Puerto de conexion no ingresado")
    exit()

directorio, puerto, show = parametros(cmd)

# Se revisa que el directorio ingresado sea valido
if not os.path.isdir(directorio):
    print(Fore.RED + f"[-] Directorio \"{directorio}\" no encontrado")
    exit()

# Se inicia la aplicacion Flask
app = Flask(__name__,
            static_url_path='',
            static_folder='.')

@app.route('/')
def main():
    nombre = getNombre(directorio) # Se obtiene el nombre del directorio
    tam = len(os.listdir(directorio)) # Se obtiene el numero de archivos del directorio

    # Se crea una 'response' html para regresar al cliente
    response = "<head>"
    response += f"<title> {nombre} - {tam} elementos </title>"
    response += f"<meta charset=\"utf-8\">"
    response += """<style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: rgb(100, 100, 100);
        }

        .galeria {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            width: 95%;
            margin: auto;
            row-gap: 10px;
            column-gap: 10px;
            padding: 40px 0;
            overflow: hidden;
        }

        .galeria img {
            border-radius: 10%;
            width: 100%;
            vertical-align: top;
            height: 300px;
            object-fit: cover;
            display: block;
            position: relative;
            overflow: hidden;
        }

        .galeria video {
            border-radius: 10px;
            width: 100%;
            vertical-align: top;
            height: 300px;
            object-fit: cover;
            display: block;
            position: relative;
            overflow: hidden;
        }

        .galeria audio {
            border-radius: 10%;
            width: 100%;
            vertical-align: top;
            height: 300px;
            object-fit: cover;
            display: block;
            position: relative;
            overflow: hidden;
        }


        .galeria a img {
            border-radius: 10%;
            width: 100%;
            vertical-align: top;
            height: 300px;
            object-fit: cover;
            display: block;
            position: relative;
            overflow: hidden;
        }
    </style>"""
    response += "</head>"
    response += f"<h1> {nombre} - {tam} elementos </h1> <hr>" # Se agrega a la 'response' el contenido de la pagina
    if show: # Si el usuario quiere mostrar graficamente los elementos...
        response += "<section class=\"galeria\">"
        archivos = os.listdir(directorio)
        archivos.sort(key=str.lower)
        for i in archivos:
            response += getResponseFile(i) # Se agrega a la 'response' una etiqueta dependiendo del archivo
        response += "</section>" # Termina el cuerpo de la 'response'

    else: # Si el usuario quiere los enlaces a los archivos
        response += f"<ul>"
        archivos = os.listdir(directorio)
        archivos.sort(key=str.lower)
        for i in archivos:
            # Se agrega a la 'response' un href con el nombre del archivo o directorio
            href = i.replace(' ', "%20")
            if os.path.isdir(f"{directorio}/{i}"):
                response += f"<li> <a href={href}> {i}/ </a> </li>"
            else:
                response += f"<li> <a href={href}> {i} </a> </li>"
        response += "</ul>" # Termina el cuerpo de la 'response'

    return response # Se regresa la 'response'

@app.route("/<string:file>") # Si se da click al enlace de un archivo, se regresa el contenido de esta
def archivo(file):
    # Se regresa un archivo al cliente
    return send_from_directory(directorio, path=file, as_attachment=False)

app.run(host="0.0.0.0", port=puerto, debug=True) # Se corre la aplicacion Flask

