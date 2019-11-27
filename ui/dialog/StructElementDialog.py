import os
from enum import IntEnum
import cv2 as cv
import numpy as np
from PyQt5 import Qt, QtGui
from PyQt5.QtCore import QRect, pyqtSignal
from PyQt5.QtGui import QIntValidator, QIcon, QCursor, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QWidget, QGridLayout, QHBoxLayout, \
    QFileDialog

from util import Actions


class SEAction(IntEnum):
    INIT = 0
    INCREASE = 1
    DECREASE = 2


class LineEditButton(QLineEdit):
    change_focus_sig = pyqtSignal(QWidget)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.change_focus_sig.emit(self)


class StructElementDialog(QDialog):
    __width = 380
    __height = 320
    grid_mat: np.ndarray
    grid_box_layout: QGridLayout

    minus_disable_icon_url = "./resource/minus_disable_icon.png"
    minus_icon_url = "./resource/minus_icon.png"
    plus_disable_icon_url = "./resource/plus_disable_icon.png"
    plus_icon_url = "./resource/plus_icon.png"
    openMaskTitle = "选择Mask"

    decrease_btn: QPushButton
    increase_btn: QPushButton
    grid_box: QWidget
    origin: tuple
    MIN_GRID_SZ = 3
    MAX_GRID_SZ = 8
    mask_url: str
    mask_label: QLabel
    mask_pixmap_box: QLabel
    mask_preview: QPixmap
    n: int = 1

    def __init__(self, parent, action):
        super(QDialog, self).__init__(parent)
        self.action = action
        self.plus_icon = QIcon(self.plus_icon_url)
        self.plus_disable_icon = QIcon(self.plus_disable_icon_url)
        self.minus_icon = QIcon(self.minus_icon_url)
        self.minus_disable_icon = QIcon(self.minus_disable_icon_url)
        self.mask_dialog = QFileDialog(self)
        self.init_ui(action)

    def init_ui(self, action):
        self.setGeometry(QRect(self.parent().geometry().x() + ((self.parent().width() - self.__width) >> 1),
                               self.parent().geometry().y() + ((self.parent().height() - self.__height) >> 1),
                               self.__width, self.__height))
        self.setWindowFlags(Qt.Qt.WindowCloseButtonHint | Qt.Qt.Dialog)
        self.setWindowTitle("自定义结构元")
        self.setStyleSheet("background-color: #fff")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 0, 30, 0)
        self.setLayout(layout)

        # Grid box
        self.grid_box = QWidget(self)
        self.grid_box_layout = QGridLayout()
        self.grid_box_layout.setContentsMargins(0, 36, 0, 0)
        self.grid_box_layout.setHorizontalSpacing(0)
        self.grid_box_layout.setVerticalSpacing(0)
        self.draw_grid_se(self.grid_box_layout, SEAction.INIT)
        self.grid_box.setStyleSheet("QLineEdit {\
                                        background: #f2f2f2;\
                                        border: 2px solid #fff;\
                                    }\
                                    QLineEdit:hover{\
                                        border: 2px solid #CFE0FF;\
                                    }")
        self.grid_box.setLayout(self.grid_box_layout)
        layout.addWidget(self.grid_box)

        self.decrease_btn = QPushButton(self)
        self.decrease_btn.setIcon(self.minus_disable_icon)
        self.increase_btn = QPushButton(self)
        self.increase_btn.setIcon(self.plus_icon)

        self.decrease_btn.setStyleSheet("height: 24px;\
                                         width: 112px;\
                                         background: #fafafa;\
                                         border-width: 1px;\
                                         border-style: flat;\
                                         border-top-left-radius: 12px;\
                                         border-bottom-left-radius: 12px")
        self.increase_btn.setStyleSheet("height: 24px;\
                                         width: 112px;\
                                         background: #f0f0f0;\
                                         border-width: 1px;\
                                         border-style: flat;\
                                         border-top-right-radius: 12px;\
                                         border-bottom-right-radius: 12px")
        self.increase_btn.setCursor(QCursor(Qt.Qt.PointingHandCursor))
        self.increase_btn.clicked.connect(self.on_increase_btn_clicked)
        self.decrease_btn.clicked.connect(self.on_decrease_btn_clicked)
        inc_dec_box = QWidget(self)
        inc_dec_box.setStyleSheet("margin-top: 32px;")
        inc_dec_box_layout = QHBoxLayout()
        inc_dec_box_layout.setSpacing(2)
        inc_dec_box_layout.setContentsMargins(0, 0, 0, 0)
        inc_dec_box.setLayout(inc_dec_box_layout)
        inc_dec_box_layout.addStretch(1)
        inc_dec_box_layout.addWidget(self.decrease_btn)
        inc_dec_box_layout.addWidget(self.increase_btn)
        inc_dec_box_layout.addStretch(1)
        layout.addWidget(inc_dec_box)

        if self.action == Actions.EROSION_RECONSTRUCT or self.action == Actions.DILATION_RECONSTRUCT:
            mask_btn_box = QWidget(self)
            mask_btn_box_layout = QHBoxLayout()
            mask_btn_box.setLayout(mask_btn_box_layout)
            mask_btn_box_layout.setContentsMargins(0, 20, 0, 0)

            mask_open_btn = QPushButton("设置Mask", mask_btn_box)
            mask_open_btn.clicked.connect(self.open_mask)
            self.mask_label = QLabel(mask_btn_box)
            mask_btn_box_layout.addWidget(mask_open_btn)
            mask_btn_box_layout.addWidget(self.mask_label)
            self.mask_pixmap_box = QLabel(self)
            self.mask_pixmap_box.setAlignment(Qt.Qt.AlignHCenter | Qt.Qt.AlignVCenter)
            layout.addWidget(mask_btn_box)
            layout.addWidget(self.mask_pixmap_box)

        if self.action == Actions.OPEN_RECONSTRUCT or self.action == Actions.CLOSE_RECONSTRUCT:
            n_edit_box = QWidget(self)
            n_edit_box_layout = QHBoxLayout()
            n_edit_box.setStyleSheet("QLineEdit{\
                                    height: 24px; border: 2px solid #999;font-size:18px; \
                                    padding-left: 8px;\
                                    } \
                                    QLineEdit:hover {border: 2px solid #666}\
                                    QLineEdit:focus {border: 2px solid #0078d7}\
                                    QLabel{font-size: 18px; max-height: 24px；margin-right: 20px}")
            n_edit_box.setLayout(n_edit_box_layout)
            n_label = QLabel("n(膨胀/腐蚀次数)", n_edit_box)
            n_edit = QLineEdit(n_edit_box)
            n_edit.setValidator(QIntValidator())
            n_edit.textChanged.connect(self.set_n)
            n_edit_box_layout.addWidget(n_label)
            n_edit_box_layout.addWidget(n_edit)
            n_edit_box_layout.setContentsMargins(0, 32, 0, 0)
            layout.addWidget(n_edit_box)

        ok_btn = QPushButton("确定", self)
        ok_btn.setStyleSheet("QPushButton{\
                                background-color: #0078d7;  \
                                height: 40px; \
                                color: #fff;\
                                margin-bottom: 40px;\
                                margin-top: 30px;\
                                border: none\
                            }\
                            QPushButton:hover{\
                                background-color: rgb(66,156,227);  \
                            }")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        layout.addStretch(1)
        self.accepted.connect(lambda: self.parent().on_se_dialog_ok(
            self.action, self.grid_mat, self.origin,
            cv.imread(self.mask_url, cv.IMREAD_UNCHANGED) if self.action == Actions.EROSION_RECONSTRUCT
            or self.action == Actions.DILATION_RECONSTRUCT else None, self.n))

    def draw_grid_se(self, layout: QGridLayout, action=SEAction.INIT):
        if action == SEAction.INIT:
            self.grid_mat = np.ones([self.MIN_GRID_SZ, self.MIN_GRID_SZ], np.int)
            self.origin = (1, 1)
        elif action == SEAction.INCREASE:
            tmp = np.ones([self.grid_mat.shape[0] + 1, self.grid_mat.shape[1] + 1], np.int)
            for i in range(self.grid_mat.shape[0]):
                for j in range(self.grid_mat.shape[1]):
                    tmp[i][j] = self.grid_mat[i][j]
            self.grid_mat = tmp
        elif action != SEAction.DECREASE:
            print("Action undefined!")
        else:
            self.grid_mat = np.copy(self.grid_mat[:-1, :-1])

        for child in self.grid_box.children():
            if type(child) == LineEditButton:
                child.deleteLater()
                self.grid_box_layout.removeWidget(child)
        for x in range(self.grid_mat.shape[0]):
            for y in range(self.grid_mat.shape[1]):
                grid_cell = LineEditButton(str(self.grid_mat[x][y]), self.grid_box)
                grid_cell.setText(str(self.grid_mat[x][y]))
                grid_cell.setAlignment(Qt.Qt.AlignVCenter | Qt.Qt.AlignHCenter)
                if self.origin == (x, y):
                    grid_cell.setStyleSheet("width: 70px; height: 40px;border: 2px solid #0074df;")
                else:
                    grid_cell.setStyleSheet("width: 70px; height: 40px;")
                grid_cell.setValidator(QIntValidator())
                grid_cell.change_focus_sig.connect(lambda widget, x=x, y=y: self.on_origin_changed(x, y, widget))
                grid_cell.textEdited.connect(lambda text, x=x, y=y: self.on_txt_edited(text, x, y))

                layout.addWidget(grid_cell, x, y, 1, 1)

    def on_increase_btn_clicked(self):
        print(self.grid_mat.shape)
        if self.grid_mat.shape[0] < self.MAX_GRID_SZ:
            self.draw_grid_se(self.grid_box_layout, SEAction.INCREASE)
            if self.grid_mat.shape[0] >= self.MAX_GRID_SZ:
                self.increase_btn.setStyleSheet("height: 24px;\
                                                 width: 112px;\
                                                 background: #fafafa;\
                                                 border-width: 1px;\
                                                 border-style: flat;\
                                                 border-top-right-radius: 12px;\
                                                 border-bottom-right-radius: 12px;")
                self.increase_btn.setIcon(self.plus_disable_icon)
                self.increase_btn.setCursor(QCursor(Qt.Qt.ArrowCursor))
            self.decrease_btn.setStyleSheet("height: 24px;\
                                             width: 112px;\
                                             background: #f0f0f0;\
                                             border-width: 1px;\
                                             border-style: flat;\
                                             border-top-left-radius: 12px;\
                                             border-bottom-left-radius: 12px")
            self.decrease_btn.setCursor(QCursor(Qt.Qt.PointingHandCursor))
            self.decrease_btn.setIcon(self.minus_icon)

    def on_decrease_btn_clicked(self):
        print(self.grid_mat.shape)
        if self.grid_mat.shape[0] > self.MIN_GRID_SZ:
            self.draw_grid_se(self.grid_box_layout, SEAction.DECREASE)
            if self.grid_mat.shape[0] <= self.MIN_GRID_SZ:
                self.decrease_btn.setStyleSheet("height: 24px;\
                                                 width: 112px;\
                                                 background: #fafafa;\
                                                 border-width: 1px;\
                                                 border-style: flat;\
                                                 border-top-left-radius: 12px;\
                                                 border-bottom-left-radius: 12px")
                self.decrease_btn.setCursor(QCursor(Qt.Qt.ArrowCursor))
                self.decrease_btn.setIcon(self.minus_disable_icon)

            self.increase_btn.setStyleSheet("height: 24px;\
                                            width: 112px;\
                                            background: #f0f0f0;\
                                            border-width: 1px;\
                                            border-style: flat;\
                                            border-top-right-radius: 12px;\
                                            border-bottom-right-radius: 12px;")
            self.increase_btn.setIcon(self.plus_icon)
            self.increase_btn.setCursor(QCursor(Qt.Qt.PointingHandCursor))

    def on_txt_edited(self, txt, i, j):
        if txt != "":
            self.grid_mat[i][j] = int(txt)
            print(self.origin, self.grid_mat)

    def on_origin_changed(self, x, y, widget):
        self.grid_box_layout.itemAtPosition(self.origin[0], self.origin[1]).widget().setStyleSheet("\
                                    QLineEdit {\
                                        background: #f2f2f2;\
                                        border: 2px solid #fff;\
                                        width:70px;\
                                        height: 40px\
                                    }\
                                    QLineEdit:hover{\
                                        border: 2px solid #CFE0FF;\
                                    }")
        self.origin = (x, y)
        self.grid_box_layout.itemAtPosition(x, y).widget().setStyleSheet("\
                                            QLineEdit {\
                                                background: #f2f2f2;\
                                                border: 2px solid #0074df;\
                                                width:70px;\
                                                height: 40px\
                                            }")
        print(self.origin, self.grid_mat)

    def set_mask(self, file_url: str):
        self.mask_url = file_url
        self.mask_preview = QPixmap(self.mask_url)
        self.mask_pixmap_box.setPixmap(self.mask_preview)
        self.mask_label.setText(self.mask_url)

    def open_mask(self):
        image, image_t = QFileDialog.getOpenFileName(self.parent(), self.openMaskTitle, os.getcwd(),
                                                     "Image Files(*.jpg *.jpeg *.png)")
        if image != "":
            self.set_mask(image)

    def set_n(self, txt):
        if txt == "":
            self.n = 0
        else:
            self.n = int(txt)
