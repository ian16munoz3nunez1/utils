from flask import Flask, send_from_directory
import os
import sys
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(nombre)
    return nombre

def getResponseFile(ubicacion):
    href = ubicacion.replace(' ', '%20')
    if isImage(ubicacion):
        return f"<img src=\"{ubicacion}\"></img>"
    elif isVideo(ubicacion):
        return f"<video src=\"{ubicacion}\" preload=\"none\" controls loop></video>"
    elif isAudio(ubicacion):
        return f"<audio src=\"{ubicacion}\" controls></audio>"

    elif ubicacion.endswith(".ino"):
        return f"<a href={href}> <img src=\".httpServer/arduino.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".c"):
        return f"<a href={href}> <img src=\".httpServer/c.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".cpp"):
        return f"<a href={href}> <img src=\".httpServer/cpp.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif ubicacion.endswith(".css"):
        return f"<a href={href}> <img src=\".httpServer/css.png\"></img> <br> <b>{ubicacion}</b> </a>"
    elif os.path.isdir(f"{directorio}/{ubicacion}"):
        return f"<img src=\".httpServer/dir.png\"></img> <br> <b>{ubicacion}</b>"
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
        return f"<a href={href}> <b>{ubicacion}</b> </a>"

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

puerto = int(sys.argv[1])
if len(sys.argv) == 2:
    directorio = os.getcwd()
elif len(sys.argv) == 3:
    directorio = os.getcwd()
    show = int(sys.argv[2])
elif len(sys.argv) == 4:
    show = int(sys.argv[2])
    directorio = os.getcwd() + '/' + sys.argv[3]


if os.path.isdir(directorio):
    app = Flask(__name__,
                static_url_path='',
                static_folder='.')

    @app.route("/")
    def principal():
        nombre = getNombre(directorio)
        tam = len(os.listdir(directorio))
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
                border-radius: 10%;
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
        response += f"<h1> {nombre} - {tam} elementos </h1> <hr>"
        if show == 1:
            response += "<section class=\"galeria\">"
            for i in os.listdir(directorio):
                if show == 1:
                    response += getResponseFile(i)
            response += "</section>"

        else:
            response += f"<ul>"
            for i in os.listdir(directorio):
                href = i.replace(' ', "%20")
                if os.path.isdir(f"{directorio}/{i}"):
                    response += f"<li> <a href={href}> {i}/ </a> </li>"
                else:
                    response += f"<li> <a href={href}> {i} </a> </li>"
            response += "</ul>"

        return response

    @app.route("/<string:file>")
    def archivo(file):
        return send_from_directory(directorio, path=file, as_attachment=False)

    app.run(host="0.0.0.0", port=puerto, debug=True)

else:
    print(Fore.YELLOW + f"[!] Directorio \"{directorio}\" no encontrado")
