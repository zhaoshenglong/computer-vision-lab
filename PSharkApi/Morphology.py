from PSharkApi.MorphologyBasic import __erosion, __dilation, __join, __union
import numpy as np
import cv2 as cv


def _is_smooth(se: np.ndarray) -> bool:
    height, width = se.shape[:2]
    for i in range(height):
        for j in range(width):
            v = se[i][j]
            if v != 1 and v != 0 and v != 255:
                return False
    return True


def morphology_dilation(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    smooth = _is_smooth(se)
    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin, smooth)
    return res


def morphology_erosion(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    smooth = _is_smooth(se)
    for i in range(height):
        for j in range(width):
            res[i][j] = __erosion(src, se, i, j, origin, smooth)
    return res


def morphology_opening(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    smooth = _is_smooth(se)
    if not smooth:
        res = morphology_erosion(src, se, origin)
        res = morphology_dilation(res, se, origin)
    else:
        res = morphology_erosion_b(src, se, origin)
        res = morphology_dilation_b(res, se, origin)
    return res


def morphology_closing(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    smooth = _is_smooth(se)
    if not smooth:
        res = morphology_dilation(src, se, origin)
        res = morphology_erosion(res, se, origin)
    else:
        res = morphology_dilation_b(src, se, origin)
        res = morphology_erosion_b(res, se, origin)
    return res


def morphology_dilation_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("not a binary image")
    assert(_is_smooth(se))

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin, True)
    return res


def morphology_erosion_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")
    assert (_is_smooth(se))

    for i in range(height):
        for j in range(width):
            res[i][j] = __erosion(src, se, i, j, origin, True)
    return res


def morphology_opening_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")
    assert (_is_smooth(se))

    res = morphology_erosion_b(src, se, origin)
    res = morphology_dilation_b(res, se, origin)
    return res


def morphology_closing_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    res: np.ndarray
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")
    assert (_is_smooth(se))

    res = morphology_dilation_b(src, se, origin)
    res = morphology_erosion_b(res, se, origin)
    return res


# Edge detection
def standard_edge_detect_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin, True) - __erosion(src, se, i, j, origin, True)
    return res


def external_edge_detect_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("external edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = __dilation(src, se, i, j, origin, True) - src[i, j]
    return res


def internal_edge_detection_b(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("internal edge detection requires grayscale image")

    for i in range(height):
        for j in range(width):
            res[i][j] = src[i][j] - __erosion(src, se, i, j, origin, True)
    return res


# Conditional dilation in binary image
# M < V (Here, suppose we are using opening operation)
def binary_conditional_dilation(M: np.ndarray, V: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    assert (M.shape == V.shape)

    stable: bool = False
    T: np.ndarray = np.copy(M)

    while not stable:
        M = morphology_dilation_b(M, se, origin)
        M = __join(M, V)
        stable = np.array_equal(M, T)
        T = np.copy(M)
    return T


# Gray scale Reconstruction
def grayscale_dilation_reconstruction(M: np.ndarray, V: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    assert (M.shape == V.shape)

    stable: bool = False
    T: np.ndarray = np.copy(M)

    while not stable:
        M = morphology_dilation(M, se, origin)
        M = __join(M, V)
        stable = np.array_equal(M, T)
        T = np.copy(M)
    return T


# Gray scale Reconstruction
def grayscale_erosion_reconstruction(M: np.ndarray, V: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    assert (M.shape == V.shape)

    stable: bool = False
    T: np.ndarray = np.copy(M)

    while not stable:
        M = morphology_erosion(M, se, origin)
        M = __union(M, V)
        stable = np.array_equal(M, T)
        T = np.copy(M)
    return T


# Gray scale Reconstruction
def grayscale_opening_reconstruction(img: np.ndarray, se: np.ndarray, origin: tuple, n: int) -> np.ndarray:
    img_copy = np.copy(img)
    for i in range(n):
        img = morphology_erosion(img, se, origin)
    return grayscale_dilation_reconstruction(img, img_copy, np.ones([4, 4]), (1, 1))


# Gray scale Reconstruction
def grayscale_closing_reconstruction(img: np.ndarray, se: np.ndarray, origin: tuple, n: int) -> np.ndarray:
    img_copy = np.copy(img)
    for i in range(n):
        img = morphology_dilation(img, se, origin)
    return grayscale_erosion_reconstruction(img, img_copy, np.ones([4, 4]), (1, 1))


# Gradient
def standard_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("standard gradient requires grayscale image")

    smooth = _is_smooth(se)
    for i in range(height):
        for j in range(width):
            res[i][j] = int(int(__dilation(src, se, i, j, origin, smooth)) -
                            __erosion(src, se, i, j, origin, smooth)) >> 1
            if res[i][j] < 0:
                res[i][j] = 0
    return res


def external_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("external gradient requires grayscale image")

    smooth = _is_smooth(se)
    for i in range(height):
        for j in range(width):
            res[i][j] = int(int(__dilation(src, se, i, j, origin, smooth)) - src[i][j]) >> 1
            if res[i][j] < 0:
                res[i][j] = 0
    return res


def internal_gradient(src: np.ndarray, se: np.ndarray, origin: tuple) -> np.ndarray:
    height, width = src.shape[:2]
    res = np.empty([height, width], src.dtype)
    if src.shape.__len__() > 2:
        raise TypeError("internal gradient requires grayscale image")

    smooth = _is_smooth(se)
    for i in range(height):
        for j in range(width):
            res[i][j] = int(int(src[i][j]) - __erosion(src, se, i, j, origin, smooth)) >> 1
            if res[i][j] < 0:
                res[i][j] = 0
    return res


def main():
    img = cv.imread("../opening.jpg", cv.IMREAD_GRAYSCALE)
    # ret, img = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
    cv.imshow("origin", img)
    img_copy = np.copy(img)

    se = np.ones([1, 5])

    # cv.imshow("dilation", morphology_dilation_b(img, se, (1, 1)))
    # cv.imshow("open", morphology_opening_b(img, se, (1, 1)))
    # cv.imshow("close", morphology_closing_b(img, se, (1, 1)))
    # cv.imshow("standard", standard_edge_detect_b(img, se, (1, 1)))
    # cv.imshow("external", external_edge_detect_b(img, se, (1, 1)))
    # cv.imshow("internal", internal_edge_detection_b(img, se, (1, 1)))
    # i = grayscale_opening_reconstruction(img, se, (1, 1), 2)
    # cv.imshow("erosion", i)
    a_se = np.ones([4, 4])
    # cv.imshow("dilated", grayscale_dilation_reconstruction(img, img_copy, a_se, (0, 1)))
    # cv.imshow("open", grayscale_opening_reconstruction(img_copy, se, (0, 1), 6))

    close_img = cv.imread("../closing.jpg", cv.IMREAD_GRAYSCALE)
    cv.imshow("close", grayscale_closing_reconstruction(close_img, a_se, (1, 1), 5))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
