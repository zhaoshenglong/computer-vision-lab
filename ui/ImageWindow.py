from typing import Dict

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
import numpy as np
import cv2 as cv

import PSharkApi
from EditHistoryCtrl import HistoryCtrl
from util import Actions, Image


class ImageWindow(QWidget):
    img_url: str = ""
    history_ctrl: HistoryCtrl

    __width: int
    __height: int
    __margin = 40
    is_right_window_open = False
    mode: int

    img_box: QLabel
    pixmap: QPixmap
    __img_edit_sig = pyqtSignal()

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
        # self.draw_pixmap("./resource/icon.png")
        layout.addWidget(self.img_box)
        layout.addStretch(1)
        self.setLayout(layout)

        self.__img_edit_sig.connect(self.parent().imageEditEvent)

    def draw_pixmap(self, img_path):
        if img_path != "":
            self.pixmap = QPixmap(img_path)
            self.img_box.setPixmap(self.pixmap)
        else:
            pass

    def draw_pixmap_cv(self, img: QImage):
        self.pixmap = QPixmap.fromImage(img)
        self.img_box.setPixmap(self.pixmap)

    def on_image_open(self, img_path: str):
        img_array = cv.imread(img_path, cv.IMREAD_UNCHANGED)
        self.img_url = img_path
        self.history_ctrl.clear()
        self.history_ctrl.push(img_array, "打开 %s" % img_path[img_path.rfind("/") + 1:])
        self.draw_pixmap(img_path)
        self.parent().menubar.toggle_undo_btn()
        self.parent().menubar.toggle_redo_btn()

    def on_image_edit(self, action: int, param: Dict = None):
        ks: int
        sigma: float
        img_array: np.ndarray
        if self.history_ctrl.is_empty():
            return
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
            img_array = PSharkApi.meanFilter(self.history_ctrl.current(), param["ks"])
            self.history_ctrl.push(img_array, "均值滤波")
        elif action == Actions.MEDIAN_FILTER:
            img_array = PSharkApi.medianFilter(self.history_ctrl.current(), param["ks"])
            self.history_ctrl.push(img_array, "中值滤波")
        elif action == Actions.GAUSSIAN_FILTER:
            img_array = PSharkApi.gaussianFilter(self.history_ctrl.current(), param["ks"], param["sigma"])
            self.history_ctrl.push(img_array, "高斯滤波")
        elif action == Actions.RGB:
            # img_array = cv.cvtColor(self.history_ctrl.current(), cv.COLOR_GRAY2RGB)
            # self.history_ctrl.push(img_array, "转化成RGB")
            pass
        elif action == Actions.GRAYSCALE:
            if type(self.history_ctrl.current()[0][0]) == np.ndarray:
                img_array = cv.cvtColor(self.history_ctrl.current(), cv.COLOR_RGB2GRAY)
                self.history_ctrl.push(img_array, "转化成GRAYSCALE")
        elif action == Actions.BINARY:
            if type(self.history_ctrl.current()[0][0]) == np.ndarray:
                ret, img_array = cv.threshold(self.history_ctrl.current(), 0, 255, cv.THRESH_OTSU)
                self.history_ctrl.push(img_array, "转化成BINARY")
        elif action == Actions.STANDARD_EDGE:
            img_array = PSharkApi.standard_edge_detect_b(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像标准边缘检测")
        elif action == Actions.EXTERNAL_EDGE:
            img_array = PSharkApi.external_edge_detect_b(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像external边缘检测")
        elif action == Actions.INTERNAL_EDGE:
            img_array = PSharkApi.internal_edge_detection_b(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像internal边缘检测")
        elif action == Actions.CONDITIONAL_DILATION:
            img_array = PSharkApi.binary_conditional_dilation(
                PSharkApi.morphology_opening_b(self.history_ctrl.current(), param["se"], param["origin"]),
                self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像条件膨胀")
        elif action == Actions.STANDARD_GRADIENT:
            img_array = PSharkApi.standard_gradient(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "灰度图像标准梯度")
        elif action == Actions.EXTERNAL_GRADIENT:
            img_array = PSharkApi.external_gradient(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "灰度图像external梯度")
        elif action == Actions.INTERNAL_GRADIENT:
            img_array = PSharkApi.internal_gradient(self.history_ctrl.current(), param["se"], param["origin"])
            self.history_ctrl.push(img_array, "灰度图像internal梯度")
        elif action == Actions.CLOSE_RECONSTRUCT:
            img_array = PSharkApi.grayscale_closing_reconstruction(
                self.history_ctrl.current(), param["se"], param["origin"], param["n"])
            self.history_ctrl.push(img_array, "二值图像标准边缘检测")
        elif action == Actions.OPEN_RECONSTRUCT:
            img_array = PSharkApi.grayscale_opening_reconstruction(
                self.history_ctrl.current(), param["se"], param["origin"], param["n"])
            self.history_ctrl.push(img_array, "二值图像标准边缘检测")
        elif action == Actions.DILATION_RECONSTRUCT:
            img_array = PSharkApi.grayscale_dilation_reconstruction(
                self.history_ctrl.current(), param["mask"], param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像标准边缘检测")
        elif action == Actions.EROSION_RECONSTRUCT:
            img_array = PSharkApi.grayscale_erosion_reconstruction(
                self.history_ctrl.current(), param["mask"], param["se"], param["origin"])
            self.history_ctrl.push(img_array, "二值图像标准边缘检测")
        else:
            print("No match action for %d" % action)
        self.draw_pixmap_cv(Image.from_cv_array(self.history_ctrl.current()))
        self.__img_edit_sig.emit()
        self.parent().menubar.toggle_undo_btn()
        self.parent().menubar.toggle_redo_btn()

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

    def on_undo(self):
        if not self.history_ctrl.undo_disable():
            self.history_ctrl.undo()
            self.draw_pixmap_cv(Image.from_cv_array(self.history_ctrl.current()))
        self.parent().menubar.toggle_undo_btn()
        self.parent().menubar.toggle_redo_btn()

    def on_redo(self):
        if not self.history_ctrl.redo_disable():
            self.history_ctrl.redo()
            self.draw_pixmap_cv(Image.from_cv_array(self.history_ctrl.current()))
        self.parent().menubar.toggle_undo_btn()
        self.parent().menubar.toggle_redo_btn()

    def save_image(self):
        cv.imwrite(self.img_url, self.history_ctrl.current())
        print("write ok")
