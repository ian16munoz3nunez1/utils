#!/bin/python3

import sys
import os
from random import randint
from time import sleep
from PyQt5.QtCore import Qt, QPoint, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QAction
from PyQt5.QtWidgets import QLabel


class imaged(QThread):
    update_image_signal = pyqtSignal(QPixmap)

    def __init__(self, t: int):
        super(imaged, self).__init__()
        self.imgs = []
        self.pause = False
        self.time = t

    def setImages(self, imgs: [str]):
        self.imgs = imgs

    def stop(self):
        self.pause = True

    def resume(self):
        self.pause = False

    def run(self):
        while True:
            aux = []
            while len(self.imgs) > 0:
                if not self.pause:
                    n = randint(0, len(self.imgs)-1)

                    pixmap = QPixmap(self.imgs[n])
                    pic = pixmap.scaled(400, 400, Qt.KeepAspectRatio)  # Resizing the image to 700x500 (widthXheight)
                    self.update_image_signal.emit(pic)

                    aux.append(self.imgs[n])
                    self.imgs.pop(n)
                sleep(self.time)

            self.imgs = aux


class QImage(QWidget):
    def __init__(self, imagePath: str = None, time: int = None):
        super(QImage, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        exitAction = QAction(self)
        exitAction.setShortcut("Q")
        exitAction.triggered.connect(self.close)
        self.addAction(exitAction)
        exitAction.setObjectName('exitAction')

        pauseAction = QAction(self)
        pauseAction.setShortcut("P")
        pauseAction.triggered.connect(self.pauseSlides)
        self.addAction(pauseAction)
        pauseAction.setObjectName('pauseAction')

        gridlayout = QGridLayout(self)
        gridlayout.setObjectName('gridlayout')
        self.setLayout(gridlayout)

        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setStyleSheet("QLabel { border: 5px solid magenta; background-color: black }")
        self.image.setFixedSize(400, 400)
        self.image.mousePressEvent = self.mousePressEvent_custom
        self.image.mouseMoveEvent = self.mouseMoveEvent_custom
        self.image.setObjectName('image')

        if imagePath is not None and os.path.isfile(imagePath):
            pixmap = QPixmap(imagePath)
            pic = pixmap.scaled(400, 400, Qt.KeepAspectRatio)  # Resizing the image to 700x500 (widthXheight)
            self.image.setPixmap(pic)
        if os.path.isdir(imagePath):
            self.__imgs = []
            self.__time = time if time is not None else 1
            self.showSlides(imagePath)

        gridlayout.addWidget(self.image, 0, 0, 1, 1)

        self.pause = False
        self.dragPos = QPoint()

    def mousePressEvent_custom(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent_custom(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()

    def isImg(self, path: str):
        ext = ['jpg', 'png', 'jpeg', 'webp', 'heic']
        for e in ext:
            if path.endswith(e):
                return True
        return False

    def pauseSlides(self):
        if not self.pause:
            self.pause = True
            self.imgd.stop()
        else:
            self.pause = False
            self.imgd.resume()

    def list_r_files(self, directory):
        for e in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, e)):
                self.list_r_files(os.path.join(directory, e))

            if os.path.isfile(os.path.join(directory, e)) and self.isImg(e):
                file = os.path.join(directory, e)
                if not QPixmap(file).isNull():
                    self.__imgs.append(file)

    def showSlides(self, directory):
        self.list_r_files(directory)

        try:
            self.imgd = imaged(self.__time)
            self.imgd.update_image_signal.connect(self.setImg)
            self.imgd.setImages(self.__imgs)
            self.imgd.start()

        except Exception as e:
            print(f"error: {e}")

    def setImg(self, pic: QPixmap):
        self.image.setPixmap(pic)


# class Gallery():
#     def __init__(self, n):
#         self.__app = QApplication([])
#         self.__n = n
#         self.__images = []
# 
#     def add(self, imagePath):
#         image = QImage(imagePath)
#         if len(self.__images) > self.__n-1:
#             self.__images[0].close()
#             self.__images.pop(0)
#         self.__images.append(image)
# 
#     def show(self):
#         for i in self.__images:
#             i.show()
# 
#     def close(self):
#         for i in self.__images:
#             i.close()


def isImg(path: str):
    ext = ['jpg', 'png', 'jpeg', 'webp', 'heic']
    for e in ext:
        if path.endswith(e):
            return True
    return False


if __name__ == '__main__':
    app = QApplication([])

    imgs = []
    args = sys.argv

    if len(args) <= 1:
        exit(1)

    for arg in args[1:]:
        if os.path.isfile(arg) and isImg(arg):
            imgs.append(QImage(arg))

        elif os.path.isdir(arg):
            imgs.append(QImage(arg, 1))

        else:
            print(f"Error reading the path \"{arg}\"")
            exit(1)

    for img in imgs:
        img.show()

    sys.exit(app.exec_())
