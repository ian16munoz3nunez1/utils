#!/bin/python3

import os
import cv2 as cv
import numpy as np


def compare(img1: np.ndarray, img2: np.ndarray):
    equal = False
    for i in range(img1.shape[1]):
        for j in range(img1.shape[0]):
            if img1[j, i] == img2[j, i]:
                continue
            else:
                return equal

    equal = True
    return equal


class Image:
    WHITE = [255, 255, 255]
    RED = [0, 0, 255]
    GREEN = [0, 255, 0]
    BLUE = [255, 0, 0]
    YELLOW = [0, 255, 255]
    MAGENTA = [255, 0, 255]
    CYAN = [255, 255, 0]
    BLACK = [0, 0, 0]

    KERNEL_BLUR_1_9 = 0
    KERNEL_BLUR_1_25 = 1
    KERNEL_BLUR_1_49 = 2
    KERNEL_BLUR_1_81 = 3
    KERNEL_SHARPE = 4
    KERNEL_ENHANCE_EDGES = 5
    KERNEL_DETECT_EDGES = 6
    KERNEL_EMBOSSED = 7

    def __init__(self, path: str, scale: float = None):
        if os.path.isfile(path) and self.isImage(path):
            self.__main = cv.imread(path)
            if scale is None:
                self.__img = self.__main.copy()
            else:
                self.__img = cv.resize(self.__main, None, fx=scale, fy=scale)

        else:
            exit(1)

    def isImage(self, path: str):
        image = False

        if path.endswith("jpg"):
            image = True
        if path.endswith("jpeg"):
            image = True
        if path.endswith("png"):
            image = True
        if path.endswith("webp"):
            image = True

        return image

    def getImage(self):
        return self.__img

    def toRed(self):
        r = self.__img.copy()
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        return r

    def toGreen(self):
        g = self.__img.copy()
        g[:, :, 0] = 0
        g[:, :, 2] = 0
        return g

    def toBlue(self):
        b = self.__img.copy()
        b[:, :, 1] = 0
        b[:, :, 2] = 0
        return b

    def toYellow(self):
        y = self.__img.copy()
        y[:, :, 0] = 0
        return y

    def toMagenta(self):
        m = self.__img.copy()
        m[:, :, 1] = 0
        return m

    def toCyan(self):
        c = self.__img.copy()
        c[:, :, 2] = 0
        return c

    def toGrayRed(self):
        r = self.__img[:, :, 2]
        return r

    def toGrayGreen(self):
        g = self.__img[:, :, 1]
        return g

    def toGrayBlue(self):
        b = self.__img[:, :, 0]
        return b

    def toGray(self):
        return cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)

    def toMeanGray(self):
        r = self.__img[:, :, 2]
        g = self.__img[:, :, 1]
        b = self.__img[:, :, 0]

        mean = r*0.33 + g*0.33 + b*0.33
        mean = mean.astype(np.uint8)

        return mean

    def toBT601(self):
        r = self.__img[:, :, 2]
        g = self.__img[:, :, 1]
        b = self.__img[:, :, 0]

        bt_601 = r*0.299 + g*0.587 + b*0.114
        bt_601 = bt_601.astype(np.uint8)

        return bt_601

    def toBT709(self):
        r = self.__img[:, :, 2]
        g = self.__img[:, :, 1]
        b = self.__img[:, :, 0]

        bt_709 = r*0.2126 + g*0.7152 + b*0.0722
        bt_709 = bt_709.astype(np.uint8)

        return bt_709

    def toNegative(self, image=None):
        if image is not None:
            return 255 - image
        else:
            return 255 - self.__img

    def kernelFilter(self, kernel):
        if isinstance(kernel, int):
            if kernel == self.KERNEL_BLUR_1_9:
                kernel = np.ones((3, 3), dtype=np.float32) * 1/9
            elif kernel == self.KERNEL_BLUR_1_25:
                kernel = np.ones((5, 5), dtype=np.float32) * 1/25
            elif kernel == self.KERNEL_BLUR_1_49:
                kernel = np.ones((7, 7), dtype=np.float32) * 1/49
            elif kernel == self.KERNEL_BLUR_1_81:
                kernel = np.ones((9, 9), dtype=np.float32) * 1/81
            elif kernel == self.KERNEL_SHARPE:
                kernel = np.array(([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]), dtype=np.float32)
            elif kernel == self.KERNEL_ENHANCE_EDGES:
                kernel = np.array(([[0, 0, 0], [-1, 1, 0], [0, 0, 0]]), dtype=np.float32)
            elif kernel == self.KERNEL_DETECT_EDGES:
                kernel = np.array(([[0, 1, 0], [1, -4, 1], [0, 1, 0]]), dtype=np.float32)
            elif kernel == self.KERNEL_EMBOSSED:
                kernel = np.array(([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]), dtype=np.float32)

        ftr = cv.filter2D(self.__img, -1, kernel)
        return ftr

    def harris(self, maximum=0.01, color='white', dilate=False, show_corners=False):
        harris = self.__img.copy()

        gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)
        gray = np.float32(gray)

        corners = cv.cornerHarris(gray, 2, 3, 0.04)
        corners = cv.dilate(corners, None) if dilate else corners

        if color.lower() == 'white':
            color = self.WHITE
        elif color.lower() == 'red':
            color = self.RED
        elif color.lower() == 'green':
            color = self.GREEN
        elif color.lower() == 'blue':
            color = self.BLUE
        elif color.lower() == 'yellow':
            color = self.YELLOW
        elif color.lower() == 'magenta':
            color = self.MAGENTA
        elif color.lower() == 'cyan':
            color = self.CYAN

        harris[corners > maximum*corners.max()] = color

        if not show_corners:
            return harris
        else:
            return corners

    def canny(self, t1=10, t2=200):
        gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray, (3, 3), 0)
        canny = cv.Canny(image=blur, threshold1=t1, threshold2=t2)

        return canny

    def toSketch(self):
        gaus = 501

        gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)
        invert = 255 - gray

        blur = cv.GaussianBlur(invert, (gaus, gaus), 0)
        invertBlur = 255 - blur

        sketch = cv.divide(gray, invertBlur, scale=256.0)

        return sketch

    def toCartoon(self):
        gray = cv.cvtColor(self.__img, cv.COLOR_BGR2GRAY)
        blur = cv.medianBlur(gray, 5)
        edges = cv.adaptiveThreshold(blur, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)

        color = cv.bilateralFilter(self.__img, 9, 250, 250)
        cartoon = cv.bitwise_and(color, color, mask=edges)

        return cartoon
