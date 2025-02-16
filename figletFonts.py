#!python3

# Ian Mu;oz Nu;ez

import os
import getpass
import platform

usuario = getpass.getuser()

myOs = platform.system().lower()

if myOs == "linux":
    directorio = f"/home/{usuario}/figlet-fonts/"
elif myOs == "windows":
    directorio = f"C:\\users\\{usuario}\\figlet-fonts"

fonts = os.listdir(directorio)
fonts.sort()
for i in fonts:
    archivo = f"{directorio}/{i}"
    if os.path.isfile(archivo) and i.endswith(".flf"):
        texto = i[:i.index(".flf")]
        print(f"---------------->{i}<----------------")
        os.system(f"figlet \"{texto}\" -f \"{i}\" -d {directorio}")

