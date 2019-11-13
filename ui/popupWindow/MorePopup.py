from enum import IntEnum

from PyQt5 import Qt
from PyQt5.QtCore import pyqtSlot, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


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

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

    def showPopup(self):
        print("show")
        if self.status == Status.INACTIVE:
            self.status = Status.ACTIVE
            self.init_ui()
        else:
            self.status = Status.ACTIVE
            self.show()
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(QRect(self.parent().width() - self.__width, 60, self.__width, 0))
        self.animation.setEndValue(QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.animation.start()

    def hidePopup(self):
        self.status = Status.HIDE
        print("hide")
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setStartValue(QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.animation.setEndValue(QRect(self.parent().width() - self.__width, 60, self.__width, 0))
        self.animation.start()

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
        # save_other_btn.setStyleSheet("QPushButton{margin-top: 6px}")
        layout.addWidget(save_other_btn)
        adjust_sz_btn = PopupButton(QIcon(self.__adjust_size_icon_url), " 调整大小", self)
        layout.addWidget(adjust_sz_btn)
        copy_btn = PopupButton(QIcon(self.__copy_icon_url), " 复制", self)
        layout.addWidget(copy_btn)
        info_btn = PopupButton(QIcon(self.__info_icon_url), " 文件信息", self)
        # info_btn.setStyleSheet("QPushButton{margin-bottom: 6px}")
        layout.addWidget(info_btn)
        self.setLayout(layout)
