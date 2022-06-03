import cv2
import numpy
import sys
import re
import requests

def escalar(height, width):
    if height > width:
        escala = 500/height
    elif width > height:
        escala = 400/width
    else:
        escala = 400/height

    return escala

url = sys.argv[1]
extensiones = ["jpg", "png", "jpeg", "webp"]

valido = False
for i in extensiones:
    if re.search(f"[.]{i}", url):
        extension = i
        valido = True
        break

if valido:
    nombre = re.findall(f"/([a-zA-Z0-9_ ].+[.]{extension})", url)[0]
    nombre = nombre.split('/')[-1]
    print(nombre)

    req = requests.get(url)
    matriz = numpy.frombuffer(req.content, dtype=numpy.uint8)

    imagen = cv2.imdecode(matriz, -1)
    height, width = imagen.shape[:2]

    escala = escalar(height, width)
    imagen = cv2.resize(imagen, None, fx=escala, fy=escala)

    cv2.imshow(nombre, imagen)
    cv2.waitKey()
    cv2.destroyAllWindows()

else:
    print("error")
