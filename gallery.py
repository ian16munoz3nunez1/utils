#!python3

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtWidgets import QLabel

class Gallery():
    def __init__(self, n):
        self.__app = QApplication([])
        self.__n = n
        self.__images = []

    def add(self, imagePath):
        frame = QWidget()
        frame.setWindowFlags(Qt.FramelessWindowHint)
        frame.setAttribute(Qt.WA_TranslucentBackground)

        gridLayout = QGridLayout(frame)
        gridLayout.setObjectName('gridLayout')
        frame.setLayout(gridLayout)

        pixmap = QPixmap(imagePath)
        pic = pixmap.scaled(700, 500, Qt.KeepAspectRatio) # Resizing the image to 700x500 (widthXheight)

        image = QLabel(frame)
        image.setPixmap(pic)
        image.setAlignment(Qt.AlignCenter)
        image.setObjectName('image')

        gridLayout.addWidget(image, 0, 0, 1, 1)

        if len(self.__images) > self.__n-1:
            self.__images.pop(0)
        self.__images.append(frame)

    def show(self):
        for i in self.__images:
            i.show()

    def close(self):
        for i in self.__images:
            i.close()

if __name__ == '__main__':
    try:
        n = int(sys.argv[1])
        gallery = Gallery(n)

    except:
        gallery = Gallery(1)

    while True:
        imagePath = input("Insert the image path: ")

        if imagePath.lower() == 'q':
            gallery.close()
            break

        else:
            gallery.add(imagePath)
            gallery.show()

