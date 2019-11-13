from enum import IntEnum

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Status(IntEnum):
    HIDE = 0
    ACTIVE = 1


class PopupButton(QPushButton):
    pass


class MorePopup(QWidget):
    status: IntEnum = Status.HIDE
    __save_other_icon_url = "./resource/save_other_icon.png"
    __adjust_size_icon_url = "./resource/adjust_size_icon.png"
    __copy_icon_url = "./resource/copy_icon.png"
    __info_icon_url = "./resource/info_icon.png"

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.init_ui()

    def showPopup(self):
        print("show!")
        self.show()

    def hidePopup(self):
        print("hide!")
        self.hide()

    def toggle(self):
        if self.status == Status.ACTIVE:
            self.status = Status.HIDE
            self.hide()
        else:
            self.status = Status.ACTIVE
            self.show()

    def init_ui(self):
        self.setGeometry(0, 0, 200, 172)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 6, 0, 6)
        save_other_btn = PopupButton(QIcon(self.__save_other_icon_url), " 另存为", self)
        layout.addWidget(save_other_btn)
        adjust_sz_btn = PopupButton(QIcon(self.__adjust_size_icon_url), " 调整大小", self)
        layout.addWidget(adjust_sz_btn)
        copy_btn = PopupButton(QIcon(self.__copy_icon_url), " 复制", self)
        layout.addWidget(copy_btn)
        info_btn = PopupButton(QIcon(self.__info_icon_url), " 文件信息", self)
        layout.addWidget(info_btn)
        self.setLayout(layout)
