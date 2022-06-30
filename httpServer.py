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

puerto = int(sys.argv[1])
if len(sys.argv) == 2:
    directorio = os.getcwd()
else:
    directorio = os.getcwd() + '/' + sys.argv[2]

if os.path.isdir(directorio):
    app = Flask(__name__)

    @app.route("/")
    def principal():
        nombre = getNombre(directorio)
        response = f"<h1> {nombre} </h1> <hr> <ul>"
        for i in os.listdir(directorio):
            href = i.replace(' ', "%20")
            response += f"<li> <a href={href}> {i} </a> </li>"
        response += "</ul>"

        return response

    @app.route("/<string:file>")
    def archivo(file):
        return send_from_directory(directorio, path=file, as_attachment=False)

    app.run(host="0.0.0.0", port=puerto, debug=True)

else:
    print(Fore.YELLOW + f"[!] Directorio \"{directorio}\" no encontrado")
