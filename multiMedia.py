import cv2
import sys
import os
from random import randint

def escalar(height, width):
    if height > width:
        escala = 500/height
    elif width > height:
        escala = 400/width
    else:
        escala = 400/height

    return escala

def getNombre(ubicacion):
    nombre = os.path.abspath(ubicacion)
    nombre = os.path.basename(ubicacion)

    return nombre

def isImage(ubicacion):
    ext = [".jpg", ".png", ".jpeg", ".webp", ".JPG", ".PNG", ".JPEG", ".WEBP"]

    imagen = False
    for i in ext:
        if ubicacion.endswith(i):
            imagen = True
            break

    return imagen

ubicacion = sys.argv[1]

if os.path.isdir(ubicacion):
    archivos = []
    for i in os.listdir(ubicacion):
        archivo = f"{ubicacion}/{i}"
        if os.path.isfile(archivo):
            archivos.append(archivo)

    numero = randint(0, len(archivos)-1)
    archivo = archivos[numero]

    imagen = cv2.imread(archivo)
    height, width = imagen.shape[:2]

    escala = escalar(height, width)
    imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

    nombre = getNombre(archivo)
    print(archivo)
    cv2.imshow(nombre, imagen)
    cv2.waitKey()
    cv2.destroyAllWindows()

elif os.path.isfile(ubicacion):
    imagen = cv2.imread(ubicacion)
    height, width = imagen.shape[:2]

    escala = escalar(height, width)
    imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

    nombre = getNombre(ubicacion)
    cv2.imshow(nombre, imagen)
    cv2.waitKey()
    cv2.destroyAllWindows()
