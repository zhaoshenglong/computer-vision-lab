from typing import Callable

import cv2 as cv
import numpy as np


def __do_edge_detect(src: np.ndarray, _do_detect: Callable):
    width = src.shape[0]
    height = src.shape[1]
    channel = 0
    if type(src[0][0]) == np.ndarray:
        channel = src.shape[2]

    dtype = src.dtype
    img = np.empty(src.shape, dtype)
    # For coherence
    # range from 1 to width - 1
    if channel != 0:
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                for k in range(channel):
                    img[i][j][k] = _do_detect(src[i - 1: i + 2, j - 1: j + 2, k])
    else:
        print(width, height, "here")
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                img[i][j] = _do_detect(src[i - 1: i + 2, j - 1: j + 2])

    # not deal with boundary
    for i in range(width):
        img[i][0] = src[i][0]
        img[i][width - 1] = src[i][width - 1]
    for j in range(height):
        img[0][j] = src[0][j]
        img[height - 1][j] = src[height - 1][j]
    return img


def __robert_gradient(src: np.ndarray):
    t: int = np.abs(int(src[1][1]) - int(src[0][0])) + \
             np.abs(int(src[0][1]) - int(src[1][0]))
    if t > 255:
        t = 255
    return np.uint8(t)


def __sobel_gradient(src: np.ndarray):
    t: int = np.abs(int(src[0][0]) + (int(src[1][0]) << 1) + int(src[2][0])
                    - int(src[0][2]) - (int(src[1][2]) << 1) - int(src[2][2])) + \
             np.abs(int(src[0][0]) + (int(src[0][1]) << 1) + int(src[0][2])
                    - int(src[2][0]) - (int(src[2][1]) << 1) - int(src[2][2]))
    if t > 255:
        t = 255
    return np.uint8(t)


def __prewitt_gradient(src: np.ndarray):
    t: int = np.abs(int(src[0][0]) + int(src[1][0]) + int(src[2][0])
                    - int(src[0][2]) - int(src[1][2]) - int(src[2][2])) + \
             np.abs(int(src[0][0]) + int(src[0][1]) + int(src[0][2])
                    - int(src[2][0]) - int(src[2][0]) - int(src[2][2]))
    if t > 255:
        t = 255
    return np.uint8(t)


def robertOperator(src: np.ndarray):
    return __do_edge_detect(src, __robert_gradient)


def sobelOperator(src: np.ndarray):
    return __do_edge_detect(src, __sobel_gradient)


def prewittOperator(src: np.ndarray):
    return __do_edge_detect(src, __prewitt_gradient)


def main():
    img = cv.imread("../resource/lena.jpg", cv.IMREAD_UNCHANGED)
    cv.imshow("source image", img)
    cv.imshow("roberts edge", robertOperator(img))
    cv.imshow("prewitt edge", prewittOperator(img))
    cv.imshow("sobel edge", sobelOperator(img))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
