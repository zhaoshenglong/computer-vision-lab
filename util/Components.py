from PyQt5.QtWidgets import QWidget


class Components(QWidget):

    @staticmethod
    def Spacer(width, height, parent: QWidget):
        sp = QWidget(parent)
        sp.setContentsMargins(0, 0, 0, 0)
        sp.setGeometry(0, 0, width, height)
        return sp
