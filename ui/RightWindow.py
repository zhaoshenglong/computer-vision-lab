from enum import IntEnum
from PyQt5 import Qt
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, \
    QLabel, QHBoxLayout, QSlider, QButtonGroup, QAbstractButton


class Status(IntEnum):
    INACTIVE = 0
    HIDE = 1
    ACTIVE = 2


class ToolButton(QPushButton):
    pass


class Identifier(IntEnum):
    MEDIAN_FILTER = 0X7001
    MEAN_FILTER = 0X7002
    GAUSSIAN_FILTER = 0X7003
    ROBERT = 0X7004
    SOBEL = 0X7005
    PREWITT = 0X7006


'''
For simplicity, this popup only provides necessary buttons without dedicated design
'''


class RightWindow(QWidget):
    status = Status.INACTIVE
    geometry_animation = None
    __width = 320
    __height = 900

    close_btn: QPushButton
    gray_slider: QSlider
    tone_slider: QSlider
    warm_slider: QSlider
    median_filter_btn: QPushButton
    mean_filter_btn: QPushButton
    gaussian_filter_btn: QPushButton
    filter_button_group: QButtonGroup
    robert_btn: QPushButton
    sobel_btn: QPushButton
    prewitt_btn: QPushButton
    edge_detection_button_group: QButtonGroup
    close_icon_url = "./resource/close_icon.png"

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__height = self.parent().height() - 60

    def show_popup(self):
        if self.status == Status.INACTIVE:
            self.status = Status.ACTIVE
            self.init_ui()
            self.gray_slider.valueChanged.connect(self.on_gray_slider_change)
            self.tone_slider.valueChanged.connect(self.on_gray_slider_change)
            self.warm_slider.valueChanged.connect(self.on_gray_slider_change)
            self.filter_button_group.buttonReleased.connect(self.on_filter_clicked)
            self.edge_detection_button_group.buttonReleased.connect(self.on_edge_btn_clicked)
            self.close_btn.clicked.connect(self.hide_popup)
            self.close_btn.clicked.connect(self.parent().image_window.on_right_window_toggle)
        else:
            self.status = Status.ACTIVE
            self.show()
        self.geometry_animation = QPropertyAnimation(self, b"geometry")
        self.geometry_animation.setDuration(100)
        self.geometry_animation.setStartValue(QRect(self.parent().width(), 60, 0, self.__height))
        self.geometry_animation.setEndValue(
            QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.geometry_animation.start()

    def hide_popup(self):
        self.status = Status.HIDE
        self.geometry_animation.setDuration(100)
        self.geometry_animation.setStartValue(
            QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.geometry_animation.setEndValue(
            QRect(self.parent().width(), 60, 0, self.__height))
        self.geometry_animation.start()

    def toggle(self):
        if self.status == Status.ACTIVE:
            self.hide_popup()
        else:
            self.show_popup()

    def init_ui(self):
        # self.setGeometry(QRect(self.parent().width() - self.__width, 60, self.__width, self.__height))
        self.setFixedWidth(self.__width)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.draw_title(layout)
        self.draw_transfer_sec(layout)
        self.draw_flat_sec(layout)
        self.draw_edge_sec(layout)
        self.setLayout(layout)

    def draw_title(self, layout):
        header = QWidget(self)
        header.setGeometry(QRect(0, 6, self.__width, 55))
        header.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        header.setStyleSheet("background-color: #f2f2f2; padding-top: 20px;padding-bottom: 20px")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("编辑", header)
        title_label.setStyleSheet("QLabel{font-size: 24px;}")

        self.close_btn = QPushButton(self)
        self.close_btn.setIcon(QIcon(self.close_icon_url))
        self.close_btn.setStyleSheet("QPushButton{ \
                                            border: none; \
                                            margin-right: 16px; \
                                         }")
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.close_btn)
        header.setLayout(header_layout)
        layout.addWidget(header)

    def draw_transfer_sec(self, layout):
        self.setStyleSheet("*{background-color: #f2f2f2;} QLabel{  \
                                        padding-top: 10px;    \
                                        padding-left: 22px;  \
                                        font-size: 16px;     \
                                        color: #6c6c6c;      \
                                    }")
        gray_label = QLabel("颜色", self)
        gray_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.gray_slider = QSlider(Qt.Qt.Horizontal, self)
        self.gray_slider.setMinimum(-100)
        self.gray_slider.setValue(0)
        self.gray_slider.setMaximum(100)
        self.gray_slider.setTracking(True)

        tone_label = QLabel("色调", self)
        tone_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tone_slider = QSlider(Qt.Qt.Horizontal, self)
        self.tone_slider.setMinimum(-100)
        self.tone_slider.setValue(0)
        self.tone_slider.setMaximum(100)
        self.tone_slider.setTracking(True)

        warm_label = QLabel("色暖", self)
        warm_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.warm_slider = QSlider(Qt.Qt.Horizontal, self)
        self.warm_slider.setMinimum(-100)
        self.warm_slider.setValue(0)
        self.warm_slider.setMaximum(100)
        self.warm_slider.setTracking(True)
        layout.addWidget(gray_label)
        layout.addWidget(self.gray_slider)
        layout.addWidget(tone_label)
        layout.addWidget(self.tone_slider)
        layout.addWidget(warm_label)
        layout.addWidget(self.warm_slider)

    def draw_flat_sec(self, layout):
        filter_label = QLabel("滤波", self)
        filter_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_label.setStyleSheet("background-color: #f2f2f2; padding-bottom: 16px")
        layout.addWidget(filter_label)

        self.filter_button_group = QButtonGroup(self)
        button_group = QWidget(self)
        button_group.setStyleSheet("QPushButton{ \
                                        background-color: #ddd;  \
                                        height: 40px;           \
                                        border: none;           \
                                    }\
                                    QPushButton:hover{ \
                                        background-color: #0078d7;  \
                                        color: #fff; \
                                    }")
        button_group.setCursor(QCursor(Qt.Qt.PointingHandCursor))
        group_box = QHBoxLayout()
        self.median_filter_btn = QPushButton("中值", self)
        self.mean_filter_btn = QPushButton("均值", self)
        self.gaussian_filter_btn = QPushButton("高斯", self)
        self.filter_button_group.addButton(self.median_filter_btn, Identifier.MEDIAN_FILTER)
        self.filter_button_group.addButton(self.mean_filter_btn, Identifier.MEAN_FILTER)
        self.filter_button_group.addButton(self.gaussian_filter_btn, Identifier.GAUSSIAN_FILTER)
        group_box.addWidget(self.median_filter_btn)
        group_box.addWidget(self.mean_filter_btn)
        group_box.addWidget(self.gaussian_filter_btn)
        group_box.setSpacing(1)
        group_box.setContentsMargins(20, 0, 20, 0)
        button_group.setLayout(group_box)
        layout.addWidget(button_group)

    def draw_edge_sec(self, layout):
        edge_label = QLabel("边缘检测", self)
        edge_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        edge_label.setStyleSheet("background-color: #f2f2f2; padding-bottom: 16px; padding-top: 20px")
        layout.addWidget(edge_label)

        self.edge_detection_button_group = QButtonGroup(self)
        button_group = QWidget(self)
        button_group.setStyleSheet("QPushButton{ \
                                        background-color: #ddd;  \
                                        height: 40px;            \
                                        border: none;            \
                                    }\
                                    QPushButton:hover{ \
                                        background-color: #0078d7;  \
                                        color: #fff; \
                                    }")
        button_group.setCursor(QCursor(Qt.Qt.PointingHandCursor))
        group_box = QHBoxLayout()
        self.robert_btn = QPushButton("Robert", self)
        self.sobel_btn = QPushButton("Sobel", self)
        self.prewitt_btn = QPushButton("Prewitt", self)
        self.edge_detection_button_group.addButton(self.robert_btn, Identifier.ROBERT)
        self.edge_detection_button_group.addButton(self.sobel_btn, Identifier.SOBEL)
        self.edge_detection_button_group.addButton(self.prewitt_btn, Identifier.PREWITT)
        group_box.addWidget(self.robert_btn)
        group_box.addWidget(self.sobel_btn)
        group_box.addWidget(self.prewitt_btn)
        group_box.setSpacing(1)
        group_box.setContentsMargins(20, 0, 20, 0)
        button_group.setLayout(group_box)
        layout.addWidget(button_group)

        # take up remained space
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer)

    def on_gray_slider_change(self, v: int):
        # print(self.gray_slider.value())
        pass

    def on_filter_clicked(self, btn: QAbstractButton):
        print(self.filter_button_group.id(btn))

    def on_edge_btn_clicked(self, btn: QAbstractButton):
        print(self.edge_detection_button_group.id(btn))

    def on_window_resize(self, width, height):
        if self.status == Status.ACTIVE:
            self.setGeometry(width - self.__width, 60, self.__width, self.__height)
