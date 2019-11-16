from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
import numpy as np
import cv2 as cv

import PSharkApi
from EditHistoryCtrl import HistoryCtrl
from util import Actions


class ImageWindow(QWidget):
    img_url: str = ""
    history_ctrl: HistoryCtrl

    __width: int
    __height: int
    __margin = 40
    is_right_window_open = False

    img_box: QLabel
    pixmap: QPixmap
    img_edit_sig = pyqtSignal()

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.history_ctrl = HistoryCtrl()
        self.init_ui()

    def init_ui(self):
        self.__height = self.parent().height()
        print(self.__height)
        self.__width = self.parent().width()    # maximum width if width < height

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(40, 60, 40, 40)
        self.setFixedHeight(self.__height)
        self.setFixedWidth(self.__width)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addStretch(1)
        self.img_box = QLabel(self)
        # For test
        self.draw_pixmap("./resource/icon.png")
        layout.addWidget(self.img_box)
        layout.addStretch(1)
        self.setLayout(layout)

        self.img_edit_sig.connect(self.parent().imageEditEvent)

    def draw_pixmap(self, img_path):
        if img_path != "":
            self.pixmap = QPixmap(img_path)
            self.img_box.setPixmap(self.pixmap)
        else:
            pass

    def draw_pixmap_cv(self, img: QImage):
        self.pixmap = QPixmap.fromImage(img)
        print("fuck!!!!!! pixmap")
        self.img_box.setPixmap(self.pixmap)

    def on_image_open(self, img_path: str):
        img_array = cv.imread(img_path, cv.IMREAD_UNCHANGED)
        self.img_url = img_path
        self.history_ctrl.clear()
        self.history_ctrl.push(img_array, "打开 %s" % img_path[img_path.rfind("/") + 1:])
        self.draw_pixmap(img_path)

    def on_image_edit(self, action: int, param: tuple = None):
        print("action %d" % action)
        ks: int
        sigma: float
        img_array: np.ndarray
        if action == Actions.ROBERT:
            img_array = PSharkApi.robert_operator(self.history_ctrl.current())
            self.history_ctrl.push(img_array, "Robert算子")
        elif action == Actions.SOBEL:
            img_array = PSharkApi.sobel_operator(self.history_ctrl.current())
            self.history_ctrl.push(img_array, "Sobel算子")
        elif action == Actions.PREWITT:
            img_array = PSharkApi.prewitt_operator(self.history_ctrl.current())
            self.history_ctrl.push(img_array, "Prewitt算子")
        elif action == Actions.MEAN_FILTER:
            img_array = PSharkApi.meanFilter(self.history_ctrl.current(), int(param[0]))
            self.history_ctrl.push(img_array, "均值滤波")
        elif action == Actions.MEDIAN_FILTER:
            img_array = PSharkApi.medianFilter(self.history_ctrl.current(), int(param[0]))
            self.history_ctrl.push(img_array, "中值滤波")
        elif action == Actions.GAUSSIAN_FILTER:
            img_array = PSharkApi.gaussianFilter(self.history_ctrl.current(), int(param[0]), float(param[1]))
            self.history_ctrl.push(img_array, "高斯滤波")
        elif action == Actions.COLOR_ADJUST:
            print("调整颜色")
        elif action == Actions.ROTATE:
            print("旋转")
        elif action == Actions.CUT:
            print("裁剪")
        else:
            print("No match action for %d" % action)
        print("start draw")
        self.draw_pixmap_cv(self.from_cv_array(self.history_ctrl.current()))
        cv.imshow("mean", self.history_ctrl.current())
        cv.waitKey(0)
        cv.destroyAllWindows()

    def from_cv_array(self, img_array):
        height = img_array.shape[0]
        width = img_array.shape[1]
        channel = 0
        img: QImage
        if type(img_array[0][0]) == np.ndarray:
            channel = img_array.shape[2]
        print(height, width, channel)
        bytes_per_line = 3 * width
        print(height, width, channel)
        if channel == 0:
            img = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        elif channel == 3:
            img = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        elif channel == 4:
            img = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        else:
            img = QImage(img_array.data, width, height, bytes_per_line, QImage.Format_Invalid)
        return img

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass

    def on_window_resize(self, width, height):
        if self.is_right_window_open:
            self.setFixedWidth(width - 320)
            self.setFixedHeight(height)
        else:
            self.setFixedWidth(width)
            self.setFixedHeight(height)

    def on_right_window_toggle(self):
        if self.is_right_window_open:
            self.is_right_window_open = False
            self.setFixedWidth(self.parent().width())
        else:
            self.is_right_window_open = True
            self.setFixedWidth(self.parent().width() - 320)     # right_window width is 320px
