import math
from typing import Callable
import numpy as np
import cv2 as cv
from enum import IntEnum


class Filter(IntEnum):
    MEAN = 1
    MEDIAN = 2
    GAUSSIAN = 3


def __meanFilter__(region: np.ndarray, kernel=None):
    return np.mean(region)


def __medianFilter__(region: np.ndarray, kernel=None):
    return np.median(region)


def __gaussianKernel__(ks: int, sigma: float):
    kernel = np.empty([ks, ks], np.float)
    central: int = ks >> 1
    x: float
    y: float
    for i in range(ks):
        y = pow(i - central, 2)
        for j in range(ks):
            x = pow(j - central, 2)
            kernel[i][j] = math.exp(-(x + y) / (pow(sigma, 2) * 2)) / (2 * math.pi * sigma)

    kernel_sum: np.float = np.float(np.sum(kernel))
    for i in range(ks):
        for j in range(ks):
            kernel[i][j] /= kernel_sum
    print(kernel)
    return kernel


def __gaussianFilter__(region: np.ndarray, kernel: np.ndarray):
    shape = region.shape
    assert (shape == kernel.shape)
    res: region.dtype = 0

    for i in range(shape[0]):
        for j in range(shape[1]):
            res += kernel[i][j] * region[i][j]
    return res


def __doFilter__(src: np.ndarray, ks: int = 3, kernel: np.ndarray = None, _filter: Callable = None):
    shape = src.shape
    dtype = src.dtype

    res = np.empty(shape, dtype)
    half_ks = ks >> 1
    for i in range(half_ks, shape[0] - half_ks):
        for j in range(half_ks, shape[1] - half_ks):
            res[i][j] = _filter(
                src[i - half_ks: i + half_ks + 1, j - half_ks: j + half_ks + 1], kernel)

    # deal with boundary, simplest way is to ignore the boundary
    for i in range(half_ks):
        for j in range(shape[1]):
            res[i][j] = src[i][j]
            res[i + shape[0] - half_ks][j] = src[i + shape[0] - half_ks][j]
    for j in range(half_ks):
        for i in range(shape[0]):
            res[i][j] = src[i][j]
            res[i][j + shape[1] - half_ks] = src[i][j + shape[1] - half_ks]
    return res


def medianFilter(src: np.ndarray, ks: int):
    return __doFilter__(src, ks=ks, _filter=__medianFilter__)


def meanFilter(src: np.ndarray, ks: int):
    return __doFilter__(src, ks=ks, _filter=__meanFilter__)


def gaussianFilter(src: np.ndarray, ks: int, sigma: float):
    kernel: np.ndarray = __gaussianKernel__(ks, sigma)
    return __doFilter__(src, ks=ks, kernel=kernel, _filter=__gaussianFilter__)


def main():
    img = cv.imread("../resource/lena.jpg", cv.IMREAD_GRAYSCALE)
    cv.imshow("source image", img)
    cv.imshow("mean filter", meanFilter(img, 3))
    cv.imshow("median filter", medianFilter(img, 3))
    cv.imshow("gaussian filter", gaussianFilter(img, 3, 0.2))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
