import requests
import re
import sys
from colorama import init
from colorama.ansi import Fore

init(autoreset=True)

extensiones = ["jpg", "png", "jpeg", "svg", "webp", "mp4", "avi", "mkv",
    "html", "css", "txt", "dat"]
upperExtensiones = [i.upper() for i in extensiones]

url = sys.argv[1]

valido = False
i = 0
while i < len(extensiones):
    if re.search(f"[.]{extensiones[i]}", url):
        valido = True
        extension = extensiones[i]
        break
    if re.search(f"[.]{upperExtensiones[i]}", url):
        valido = True
        extension = upperExtensiones[i]
        break
    i += 1

if valido:
    nombre = re.findall(f"/([a-zA-Z0-9_ ].+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]

    req = requests.get(url)

    with open(nombre, 'wb') as archivo:
        archivo.write(req.content)
    archivo.close()
    print(Fore.GREEN + f"[+] Archivo \"{nombre}\" creado correctamente")

else:
    print(Fore.RED +  "error")
