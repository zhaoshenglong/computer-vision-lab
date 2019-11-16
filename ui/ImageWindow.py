from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
import numpy as np
import cv2 as cv

from EditHistoryCtrl import HistoryCtrl


class ImageWindow(QWidget):
    img_url: str = ""
    img_array: np.ndarray
    img_box: QLabel
    pixmap: QPixmap
    history_ctrl: HistoryCtrl
    __width: int
    __height: int
    __margin = 40
    is_right_window_open = False

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

    def draw_pixmap(self, img_path):
        if img_path != "":
            self.pixmap = QPixmap(img_path)
            self.img_box.setPixmap(self.pixmap)
        else:
            pass

    def on_image_change(self):
        pass

    def on_image_open(self, img_path: str):
        self.img_array = cv.imread(img_path, cv.IMREAD_UNCHANGED)
        self.img_url = img_path
        self.history_ctrl.clear()
        self.history_ctrl.push(self.img_array, "打开 %s" % img_path[img_path.rfind("/") + 1:])
        self.draw_pixmap(img_path)
        self.from_cv_array()

    def from_cv_array(self):
        height, width, channel = self.img_array.shape
        bytesPerLine = 3 * width
        print(height, width, channel)

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
