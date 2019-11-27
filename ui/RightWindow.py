from enum import IntEnum
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import QPropertyAnimation, QRect, QEvent
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSizePolicy, \
    QLabel, QHBoxLayout, QSlider, QButtonGroup, QAbstractButton, QScrollArea

from util import Actions


class Status(IntEnum):
    INACTIVE = 0
    HIDE = 1
    ACTIVE = 2


'''
For simplicity, this popup only provides necessary buttons without dedicated design
'''


class RightWindow(QWidget):
    status = Status.INACTIVE
    geometry_animation = None
    __width = 320
    __height = 900

    close_btn: QPushButton

    mode_button_group: QButtonGroup
    rgb_btn: QPushButton
    grayscale_btn: QPushButton
    binary_btn: QPushButton
    median_filter_btn: QPushButton
    mean_filter_btn: QPushButton
    gaussian_filter_btn: QPushButton
    filter_button_group: QButtonGroup
    robert_btn: QPushButton
    sobel_btn: QPushButton
    prewitt_btn: QPushButton
    edge_detection_button_group: QButtonGroup

    grayscale_gradient_button_group: QButtonGroup
    grayscale_gradient_standard: QPushButton
    grayscale_gradient_external: QPushButton
    grayscale_gradient_internal: QPushButton
    grayscale_reconstruct_button_group: QButtonGroup
    dilation_rec_btn: QPushButton
    erosion_rec_btn: QPushButton
    open_rec_btn: QPushButton
    close_rec_btn: QPushButton

    conditional_dilation_btn: QPushButton
    binary_edge_detection_button_group: QButtonGroup
    binary_edge_detection_standard: QPushButton
    binary_edge_detection_external: QPushButton
    binary_edge_detection_internal: QPushButton

    binary_reconstruct: QPushButton

    close_icon_url = "./resource/close_icon.png"

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.__height = self.parent().height() - 60

    def show_popup(self):
        if self.status == Status.INACTIVE:
            self.status = Status.ACTIVE
            self.init_ui()
            self.mode_button_group.buttonReleased.connect(
                lambda b: self.parent().image_window.on_image_edit(self.mode_button_group.id(b))
            )
            self.mode_button_group.buttonReleased.connect(self.on_mode_clicked)
            self.filter_button_group.buttonReleased.connect(
                lambda b: self.parent().openFilterEvent(self.filter_button_group.id(b))
            )
            self.edge_detection_button_group.buttonReleased.connect(
                lambda b: self.parent().image_window.on_image_edit(self.edge_detection_button_group.id(b)))
            self.grayscale_reconstruct_button_group.buttonReleased.connect(
                lambda b: self.parent().openSeDialogEvent(self.grayscale_reconstruct_button_group.id(b)))
            self.grayscale_gradient_button_group.buttonReleased.connect(
                lambda b: self.parent().openSeDialogEvent(self.grayscale_gradient_button_group.id(b)))
            self.binary_edge_detection_button_group.buttonReleased.connect(
                lambda b: self.parent().openSeDialogEvent(self.binary_edge_detection_button_group.id(b)))
            self.conditional_dilation_btn.clicked.connect(
                lambda b: self.parent().openSeDialogEvent(Actions.CONDITIONAL_DILATION))

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
        self.setFixedWidth(self.__width)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.draw_title(layout)
        self.draw_mode_sec(layout)
        self.draw_flat_sec(layout)
        self.draw_edge_sec(layout)
        self.draw_grayscale_sec(layout)
        self.draw_binary_sec(layout)

        # take up remained space
        spacer = QWidget(self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer)
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

    def draw_mode_sec(self, layout):
        self.setStyleSheet("*{background-color: #f2f2f2;} QLabel{  \
                                        padding-top: 10px;    \
                                        padding-left: 22px;  \
                                        padding-bottom: 10px;\
                                        font-size: 16px;     \
                                        color: #6c6c6c;      \
                                    }")
        self.mode_button_group = QButtonGroup(self)
        button_group = QWidget(self)
        button_group.setStyleSheet("QPushButton{ \
                                        background-color: #f2f2f2;  \
                                        height: 40px;           \
                                        border: none;           \
                                        border-bottom: 3px solid transparent\
                                    }\
                                    QPushButton:hover{\
                                        border-bottom: 3px solid #0074df\
                                    }")
        button_group.setCursor(QCursor(Qt.Qt.PointingHandCursor))
        group_box = QHBoxLayout()
        self.rgb_btn = QPushButton("RGB", self)
        self.grayscale_btn = QPushButton("GrayScale", self)
        self.binary_btn = QPushButton("Binary", self)

        self.mode_button_group.addButton(self.rgb_btn, Actions.RGB)
        self.mode_button_group.addButton(self.grayscale_btn, Actions.GRAYSCALE)
        self.mode_button_group.addButton(self.binary_btn, Actions.BINARY)
        group_box.addWidget(self.rgb_btn)
        group_box.addWidget(self.grayscale_btn)
        group_box.addWidget(self.binary_btn)
        group_box.setSpacing(1)
        group_box.setContentsMargins(20, 0, 20, 0)
        button_group.setLayout(group_box)
        layout.addWidget(button_group)

    def draw_flat_sec(self, layout):
        filter_label = QLabel("滤波", self)
        filter_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filter_label.setStyleSheet("background-color: #f2f2f2;")
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
        self.filter_button_group.addButton(self.median_filter_btn, Actions.MEDIAN_FILTER)
        self.filter_button_group.addButton(self.mean_filter_btn, Actions.MEAN_FILTER)
        self.filter_button_group.addButton(self.gaussian_filter_btn, Actions.GAUSSIAN_FILTER)
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
        edge_label.setStyleSheet("background-color: #f2f2f2; padding-top: 20px")
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
        self.edge_detection_button_group.addButton(self.robert_btn, Actions.ROBERT)
        self.edge_detection_button_group.addButton(self.sobel_btn, Actions.SOBEL)
        self.edge_detection_button_group.addButton(self.prewitt_btn, Actions.PREWITT)
        group_box.addWidget(self.robert_btn)
        group_box.addWidget(self.sobel_btn)
        group_box.addWidget(self.prewitt_btn)
        group_box.setSpacing(1)
        group_box.setContentsMargins(20, 0, 20, 0)
        button_group.setLayout(group_box)
        layout.addWidget(button_group)

    def draw_grayscale_sec(self, layout):
        grayscale_label = QLabel("灰度图像操作", self)
        grayscale_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        grayscale_label.setStyleSheet("background-color: #f2f2f2;\
                                        padding-top: 20px;border-bottom: 3px solid #f9f9f9")
        grayscale_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(grayscale_label)

        gradient_label = QLabel("梯度", self)
        layout.addWidget(gradient_label)
        self.grayscale_gradient_button_group = QButtonGroup(self)
        self.grayscale_gradient_standard = QPushButton("Standard", self)
        self.grayscale_gradient_external = QPushButton("external", self)
        self.grayscale_gradient_internal = QPushButton("internal", self)
        self.grayscale_gradient_button_group.addButton(
            self.grayscale_gradient_standard, Actions.STANDARD_GRADIENT)
        self.grayscale_gradient_button_group.addButton(
            self.grayscale_gradient_external, Actions.EXTERNAL_GRADIENT)
        self.grayscale_gradient_button_group.addButton(
            self.grayscale_gradient_internal, Actions.INTERNAL_GRADIENT)
        gradient_btn_group = QWidget(self)
        gradient_btn_group.setCursor(QCursor(Qt.Qt.PointingHandCursor))
        gradient_btn_box_layout = QHBoxLayout()
        gradient_btn_box_layout.setSpacing(1)
        gradient_btn_box_layout.setContentsMargins(20, 0, 20, 0)
        gradient_btn_box_layout.addWidget(self.grayscale_gradient_standard)
        gradient_btn_box_layout.addWidget(self.grayscale_gradient_external)
        gradient_btn_box_layout.addWidget(self.grayscale_gradient_internal)
        gradient_btn_group.setStyleSheet("QPushButton{ \
                                                background-color: #ddd;  \
                                                height: 40px;            \
                                                border: none;            \
                                            }\
                                            QPushButton:hover{ \
                                                background-color: #0078d7;  \
                                                color: #fff; \
                                            }")
        gradient_btn_group.setLayout(gradient_btn_box_layout)
        layout.addWidget(gradient_btn_group)

        reconstruction_label = QLabel("形态学重建", self)
        layout.addWidget(reconstruction_label)
        reconstruction_button_box = QWidget(self)
        reconstruction_box_layout = QHBoxLayout()

        self.dilation_rec_btn = QPushButton("膨胀", reconstruction_button_box)
        self.erosion_rec_btn = QPushButton("腐蚀", reconstruction_button_box)
        self.open_rec_btn = QPushButton("开", reconstruction_button_box)
        self.close_rec_btn = QPushButton("闭", reconstruction_button_box)
        reconstruction_box_layout.addWidget(self.dilation_rec_btn)
        reconstruction_box_layout.addWidget(self.erosion_rec_btn)
        reconstruction_box_layout.addWidget(self.open_rec_btn)
        reconstruction_box_layout.addWidget(self.close_rec_btn)
        reconstruction_box_layout.setSpacing(3)
        reconstruction_box_layout.setContentsMargins(20, 0, 20, 0)
        self.grayscale_reconstruct_button_group = QButtonGroup(self)
        self.grayscale_reconstruct_button_group.addButton(self.dilation_rec_btn, Actions.DILATION_RECONSTRUCT)
        self.grayscale_reconstruct_button_group.addButton(self.erosion_rec_btn, Actions.EROSION_RECONSTRUCT)
        self.grayscale_reconstruct_button_group.addButton(self.open_rec_btn, Actions.OPEN_RECONSTRUCT)
        self.grayscale_reconstruct_button_group.addButton(self.close_rec_btn, Actions.CLOSE_RECONSTRUCT)
        reconstruction_button_box.setLayout(reconstruction_box_layout)
        layout.addWidget(reconstruction_button_box)

    def draw_binary_sec(self, layout):
        binary_label = QLabel("二值图像操作", self)
        binary_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        binary_label.setStyleSheet("background-color: #f2f2f2;\
                                                padding-top: 20px;border-bottom: 3px solid #f9f9f9")
        binary_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(binary_label)

        # conditional dilation
        conditional_dilation_box = QWidget(self)
        conditional_dilation_box_layout = QHBoxLayout()
        conditional_dilation_box_layout.setSpacing(5)
        conditional_dilation_box_layout.setContentsMargins(20, 0, 20, 0)
        conditional_dilation_label = QLabel("重建", conditional_dilation_box)
        conditional_dilation_label.setStyleSheet("margin-right: 5px;padding-left:0px;")
        conditional_dilation_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.conditional_dilation_btn = QPushButton("Conditional Dilation", conditional_dilation_box)
        conditional_dilation_box_layout.addWidget(conditional_dilation_label)
        conditional_dilation_box_layout.addWidget(self.conditional_dilation_btn)
        conditional_dilation_box.setLayout(conditional_dilation_box_layout)
        layout.addWidget(conditional_dilation_box)

        # edge detection
        edge_label = QLabel("边缘检测", self)
        layout.addWidget(edge_label)
        self.binary_edge_detection_button_group = QButtonGroup(self)
        edge_detection_button_box = QWidget(self)
        edge_detection_button_box_layout = QHBoxLayout()
        edge_detection_button_box_layout.setSpacing(2)
        edge_detection_button_box_layout.setContentsMargins(20, 0, 20, 0)
        edge_detection_button_box.setLayout(edge_detection_button_box_layout)
        self.binary_edge_detection_standard = QPushButton("Standard", self)
        self.binary_edge_detection_external = QPushButton("external", self)
        self.binary_edge_detection_internal = QPushButton("internal", self)
        self.binary_edge_detection_button_group.addButton(self.binary_edge_detection_standard, Actions.STANDARD_EDGE)
        self.binary_edge_detection_button_group.addButton(self.binary_edge_detection_external, Actions.EXTERNAL_EDGE)
        self.binary_edge_detection_button_group.addButton(self.binary_edge_detection_internal, Actions.INTERNAL_EDGE)
        edge_detection_button_box_layout.addWidget(self.binary_edge_detection_standard)
        edge_detection_button_box_layout.addWidget(self.binary_edge_detection_external)
        edge_detection_button_box_layout.addWidget(self.binary_edge_detection_internal)
        layout.addWidget(edge_detection_button_box)

    def on_window_resize(self, width, height):
        if self.status == Status.ACTIVE:
            self.setGeometry(width - self.__width, 60, self.__width, self.__height)

    def on_mode_clicked(self, btn: QPushButton):
        self.mode_button_group.id(btn)
        for b in self.mode_button_group.buttons():
            b.setStyleSheet("QPushButton{ \
                                background-color: #f2f2f2;  \
                                height: 40px;            \
                                border: none;            \
                                border-bottom: 3px solid transparent\
                            }\
                            QPushButton:hover{\
                                border-bottom: 3px solid #0074df\
                            }")
        btn.setStyleSheet("QPushButton{ \
                                background-color: #f2f2f2;  \
                                height: 40px;            \
                                border: none;            \
                                border-bottom: 3px solid #0074df\
                            }")
