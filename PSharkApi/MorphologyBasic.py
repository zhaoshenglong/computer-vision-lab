from typing import List

import numpy as np
import cv2 as cv
"""
Basic morphology operations including dilation, erosion, opening, closing
"""


def __dilation(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple, smooth: bool):
    r, c = se.shape[:2]
    height, width = src.shape[:2]

    # Assume shape of src is larger that se
    res: int = 0
    if not smooth:
        for ri in range(r):
            for rj in range(c):
                a = ri - origin[0]
                b = rj - origin[1]
                if 0 <= i - a < height and 0 <= j - b < width:
                    res = max(res, int(src[i - a, j - b]) + se[ri, rj])
    else:
        for ri in range(r):
            for rj in range(c):
                a = ri - origin[0]
                b = rj - origin[1]
                if 0 <= i - a < height and 0 <= j - b < width:
                    res = max(res, int(src[i - a, j - b]))
    return res if res <= 255 else 255


def __erosion(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple, smooth: bool):
    r, c = se.shape[:2]
    height, width = src.shape[:2]

    # Assume shape of src is larger that se
    res: int = 255
    if not smooth:
        for ri in range(r):
            for rj in range(c):
                a = ri - origin[0]
                b = rj - origin[1]
                if 0 <= i + a < height and 0 <= j + b < width:
                    res = min(res, int(src[i + a, j + b]) - se[ri, rj])
    else:
        for ri in range(r):
            for rj in range(c):
                a = ri - origin[0]
                b = rj - origin[1]
                if 0 <= i + a < height and 0 <= j + b < width:
                    res = min(res, int(src[i + a, j + b]))
    return res if res > 0 else 0


# Supports only two dimensional mat
def __join(l: np.ndarray, r: np.ndarray) -> np.ndarray:
    height, width = l.shape
    res = np.empty([height, width], l.dtype)
    for i in range(height):
        for j in range(width):
            res[i][j] = min(l[i][j], r[i][j])
    return res


def __union(l: np.ndarray, r: np.ndarray) -> np.ndarray:
    height, width = l.shape
    res = np.empty([height, width], l.dtype)
    for i in range(height):
        for j in range(width):
            res[i][j] = max(l[i][j], r[i][j])
    return res


if __name__ == "__main__":
    img = cv.imread("../lena.jpg", cv.IMREAD_UNCHANGED)
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    color = cv.cvtColor(gray, cv.COLOR_GRAY2RGB)
    cv.imshow("gray", gray)
    cv.imshow("color", color)
    cv.waitKey(0)
    cv.destroyAllWindows()
