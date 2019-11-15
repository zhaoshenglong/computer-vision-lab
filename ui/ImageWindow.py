from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget


class ImageWindow(QWidget):
    image = None
    __width = 0
    __height = 0

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

    def init_ui(self):
        pass

    def on_image_change(self):
        pass

    def fromCvArray(self):
        pass

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        pass
