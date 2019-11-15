from enum import IntEnum

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QGradient, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QSpacerItem


class Status(IntEnum):
    INACTIVE = 0
    HIDE = 1
    ACTIVE = 2


class PopupButton(QPushButton):
    pass


class MorePopup(QWidget):
    status: IntEnum = Status.INACTIVE
    __save_other_icon_url = "./resource/save_other_icon.png"
    __adjust_size_icon_url = "./resource/adjust_size_icon.png"
    __copy_icon_url = "./resource/copy_icon.png"
    __info_icon_url = "./resource/info_icon.png"
    __width = 200
    __height = 160
    geometry_animation = None

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        shadow = QGraphicsDropShadowEffect(self.parent())
        shadow.setBlurRadius(50)
        shadow.setColor(QColor(190, 190, 190, 240))
        shadow.setOffset(-5, 10)
        self.setGraphicsEffect(shadow)

    def showPopup(self):
        if self.status == Status.INACTIVE:
            self.status = Status.ACTIVE
            self.init_ui()
        else:
            self.status = Status.ACTIVE
            self.show()
        self.geometry_animation = QPropertyAnimation(self, b"geometry")
        self.geometry_animation.setDuration(150)
        self.geometry_animation.setStartValue(QRect(self.parent().width() - self.__width, 60, self.__width, 0))
        self.geometry_animation.setEndValue(
            QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.geometry_animation.start()

    def hidePopup(self):
        self.status = Status.HIDE
        assert (self.geometry_animation is not None)
        self.geometry_animation.setDuration(100)
        self.geometry_animation.setStartValue(
            QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.geometry_animation.setEndValue(QRect(self.parent().width() - self.__width, 40, self.__width, 0))
        self.geometry_animation.start()

    def toggle(self):
        if self.status == Status.ACTIVE:
            self.hidePopup()
        else:
            self.showPopup()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        save_other_btn = PopupButton(QIcon(self.__save_other_icon_url), " 另存为", self)
        layout.addWidget(save_other_btn)
        adjust_sz_btn = PopupButton(QIcon(self.__adjust_size_icon_url), " 调整大小", self)
        layout.addWidget(adjust_sz_btn)
        copy_btn = PopupButton(QIcon(self.__copy_icon_url), " 复制", self)
        layout.addWidget(copy_btn)
        info_btn = PopupButton(QIcon(self.__info_icon_url), " 文件信息", self)

        layout.addWidget(info_btn)
        self.setLayout(layout)

    def on_window_clicked(self, x: int, y: int):
        if self.status == Status.ACTIVE and \
                (not self.geometry().x() - 2 < x < self.geometry().x() + self.geometry().width() + 2 or
                 not self.geometry().y() - 2 < y < self.geometry().y() + self.geometry().height() + 2):
            self.hidePopup()

    def on_window_resize(self):
        if self.status == Status.ACTIVE:
            self.hidePopup()
