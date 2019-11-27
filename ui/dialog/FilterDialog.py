from PyQt5 import Qt
from PyQt5.QtCore import QRect, QRegExp
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit

from util import Actions


class FilterDialog(QDialog):
    __width = 450
    __height = 300
    kernel_input: QLineEdit
    sigma_input: QLineEdit

    def __init__(self, parent, action):
        super(QDialog, self).__init__(parent)
        if action == Actions.GAUSSIAN_FILTER:
            self.__height = 300
        else:
            self.__height = 200
        self.action = action
        self.init_ui(action)

    def init_ui(self, action):
        self.setGeometry(QRect(self.parent().geometry().x() + ((self.parent().width() - self.__width) >> 1),
                               self.parent().geometry().y() + ((self.parent().height() - self.__height) >> 1),
                               self.__width, self.__height))
        self.setWindowFlags(Qt.Qt.WindowCloseButtonHint | Qt.Qt.Dialog)
        self.setWindowTitle("自定义kernel")
        self.setStyleSheet("QDialog{background-color: #fff}\
                            QLineEdit{\
                                    height: 40px; border: 3px solid #999;font-size:20px; \
                                    padding-left: 4px;\
                            } \
                            QLineEdit:hover {border: 3px solid #666}\
                            QLineEdit:focus {border: 3px solid #0078d7}\
                            QLabel{font-size: 18px; max-height: 40px; margin-top: 30px; margin-bottom: 10px}\
                            ")
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(30, 0, 30, 0)

        kernel_label = QLabel("kernel", self)
        self.kernel_input = QLineEdit(self)
        self.kernel_input.setValidator(QIntValidator())
        layout.addWidget(kernel_label)
        layout.addWidget(self.kernel_input)
        sigma_label: QLabel

        if action == Actions.GAUSSIAN_FILTER:
            sigma_label = QLabel("sigma", self)
            self.sigma_input = QLineEdit(self)
            self.sigma_input.setValidator(QRegExpValidator(QRegExp("[1-9][0-9]*(.)?[0-9]*"), self.sigma_input))
            layout.addWidget(sigma_label)
            layout.addWidget(self.sigma_input)
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
        layout.addWidget(ok_btn)
        self.setLayout(layout)
        ok_btn.clicked.connect(self.accept)
        if action == Actions.GAUSSIAN_FILTER:
            self.accepted.connect(lambda: self.parent()
                                  .image_window.on_image_edit(action,
                                                              (self.kernel_input.text(), self.sigma_input.text())))
        else:
            self.accepted.connect(lambda: self.parent()
                                  .image_window.on_image_edit(action,
                                                              (self.kernel_input.text())))
