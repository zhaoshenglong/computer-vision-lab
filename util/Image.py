from enum import IntEnum
import numpy as np
from PyQt5.QtGui import QImage


def from_cv_array(img_array: np.ndarray):
    height = img_array.shape[0]
    width = img_array.shape[1]
    channel = 0
    img: QImage
    if type(img_array[0][0]) == np.ndarray:
        channel = img_array.shape[2]
    print(channel)
    if channel == 0:
        print(img_array)

        img = QImage(img_array, width, height, width, QImage.Format_Grayscale8)
    elif channel == 3:
        img = QImage(img_array.data, width, height, width * 3, QImage.Format_RGB888).rgbSwapped()
    elif channel == 4:
        img = QImage(img_array.data, width, height, width * 4, QImage.Format_RGBA8888).rgbSwapped()
    else:
        print("Invalid image type")
        img = QImage(img_array.data, width, height, width, QImage.Format_Invalid)
    return img


class ImageMode(IntEnum):
    RGB888 = 0X1001
    RGB8888 = 0X1002
    GRAYSCALE = 0X1003
    BINARY = 0X1004
