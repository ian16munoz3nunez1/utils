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
        return f"<img src=\"{ubicacion}\" width=\"50%\" style=\"border-radius: 20%\"></img> <hr>"
    elif isVideo(ubicacion):
        return f"<video src=\"{ubicacion}\" width=\"50%\" controls loop></video> <hr>"
    elif isAudio(ubicacion):
        return f"<audio src=\"{ubicacion}\" width=\"50%\" controls></audio> <hr>"

    elif ubicacion.endswith(".ino"):
        return f"<a href={href}> <img src=\".httpServer/arduino.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b>  <hr>"
    elif ubicacion.endswith(".c"):
        return f"<a href={href}> <img src=\".httpServer/c.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".cpp"):
        return f"<a href={href}> <img src=\".httpServer/cpp.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".css"):
        return f"<a href={href}> <img src=\".httpServer/css.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif os.path.isdir(f"{directorio}/{ubicacion}"):
        return f"<img src=\".httpServer/dir.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".ods") or ubicacion.endswith(".xlsx"):
        return f"<a href={href}> <img src=\".httpServer/excel.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".xcf"):
        return f"<a href={href}> <img src=\".httpServer/gimp.webp\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".go"):
        return f"<a href={href}> <img src=\".httpServer/golang.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".html"):
        return f"<a href={href}> <img src=\".httpServer/html.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".java") or ubicacion.endswith(".class") or ubicacion.endswith(".jar"):
        return f"<a href={href}> <img src=\".httpServer/java.jpg\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".js"):
        return f"<a href={href}> <img src=\".httpServer/js.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".lat"):
        return f"<a href={href}> <img src=\".httpServer/latino.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".m"):
        return f"<a href={href}> <img src=\".httpServer/octave.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".pdf"):
        return f"<a href={href}> <img src=\".httpServer/pdf.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".pl"):
        return f"<a href={href}> <img src=\".httpServer/perl.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".php"):
        return f"<a href={href}> <img src=\".httpServer/php.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".odp") or ubicacion.endswith(".pptx"):
        return f"<a href={href}> <img src=\".httpServer/powerpoint.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".p"):
        return f"<a href={href}> <img src=\".httpServer/prolog.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".py"):
        return f"<a href={href}> <img src=\".httpServer/python.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".rb"):
        return f"<a href={href}> <img src=\".httpServer/ruby.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".sql"):
        return f"<a href={href}> <img src=\".httpServer/sql.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".txt") or ubicacion.endswith(".dat"):
        return f"<a href={href}> <img src=\".httpServer/txt.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    elif ubicacion.endswith(".odt") or ubicacion.endswith(".docx"):
        return f"<a href={href}> <img src=\".httpServer/word.png\" width=\"30%\" style=\"border-radius: 20%;\"></img> </a> <br> <b>{ubicacion}</b> <hr>"
    else:
        return f"<a href={href}> <b>{ubicacion}</b> </a> <hr>"

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
        response = f"<title> {nombre} - {tam} elementos </title>"
        response += f"<h1> {nombre} - {tam} elementos </h1> <hr>"
        if show == 1:
            response += "<div align=\"center\">"
            for i in os.listdir(directorio):
                if show == 1:
                    response += getResponseFile(i)
            response += "</div>"

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
