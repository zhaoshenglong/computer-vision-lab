import os

from PyQt5.QtWidgets import QFileDialog


class FileDialog:
    parent = None
    FileDialogTitle = "选择图片"

    def __init__(self, parent):
        self.parent = parent

    def open_image(self):
        image, image_t = QFileDialog.getOpenFileName(self.parent, self.FileDialogTitle, os.getcwd(),
                                                     "JPG Files(*.jpg);;JPEG Files(*.jpeg);; \
                                                    PNG Files(*.png);;")
        if image != "":
            print(image, image_t)
            return image
        else:
            print("You haven't choose a picture")

    def save_image(self):
        print("You are saving image")
