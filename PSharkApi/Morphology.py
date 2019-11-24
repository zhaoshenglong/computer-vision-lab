from PSharkApi.MorphologyBasic import __erosion, __dilation, __join, __dilation_b, __erosion_b
import numpy as np
import cv2 as cv


def morphology_dilation(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin)
    return res


def morphology_erosion(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __erosion(src, se, i, j, origin)
    return res


def morphology_opening(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    res = morphology_erosion(src, se, origin)
    res = morphology_dilation(res, se, origin)
    return res


def morphology_closing(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    res = morphology_dilation(src, se, origin)
    res = morphology_erosion(res, se, origin)
    return res


def morphology_dilation_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation_b(src, se, i, j, origin)
    return res


def morphology_erosion_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __erosion_b(src, se, i, j, origin)
    return res


def morphology_opening_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    res = morphology_erosion_b(src, se, origin)
    res = morphology_dilation_b(res, se, origin)
    return res


def morphology_closing_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    res = morphology_dilation_b(src, se, origin)
    res = morphology_erosion_b(res, se, origin)
    return res


# Edge detection
def standard_edge_detect(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin) - __erosion(src, se, i, j, origin)
    return res


def external_edge_detect(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("external edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin) - src[i, j]
    return res


def internal_edge_detection(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("internal edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = src[i][j] - __erosion(src, se, i, j, origin)
    return res


# Conditional dilation in binary image
# M < V (Here, suppose we are using opening operation)
def binary_conditional_dilation(M: np.ndarray, V: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    assert(M.shape == V.shape)

    stable: bool = False
    T: np.ndarray = np.copy(M)

    while not stable:
        M = morphology_dilation_b(M, se, origin)
        M = __join(M, V)
        stable = np.array_equal(M, T)
        T = np.copy(M)
    return T


# Gray scale Reconstruction
def grayscale_reconstruction(M: np.ndarray, V: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    assert (M.shape == V.shape)

    stable: bool = False
    T: np.ndarray = np.copy(M)

    while not stable:
        M = morphology_dilation(M, se, origin)
        M = __join(M, V)
        stable = np.array_equal(M, T)
        T = np.copy(M)
    return T


# Gradient
def standard_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard gradient requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = int(src[i][j] - __erosion(src, se, i, j, origin)) >> 1
    return res


def external_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("external gradient requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = int(src[i][j] - __erosion(src, se, i, j, origin)) >> 1
    return res


def internal_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("internal gradient requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = int(src[i][j] - __erosion(src, se, i, j, origin)) >> 1
    return res


def main():
    img = cv.imread("../lena.jpg", cv.IMREAD_GRAYSCALE)
    cv.imshow("origin", img)
    se = np.ones([3, 3])
    open_img = morphology_erosion(img, se, (1, 1))
    cv.imshow("dilated", open_img)
    cv.imshow("reconstruction", grayscale_reconstruction(open_img, img, se, (1, 1)))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()