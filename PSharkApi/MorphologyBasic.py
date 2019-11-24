from typing import List

import numpy as np

"""
Basic morphology operations including dilation, erosion, opening, closing
"""


def __dilation(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple):
    r, c = se.shape[:2]
    height, width = src.shape[:2]

    # Assume shape of src is larger that se
    res = 0
    for ri in range(r):
        for rj in range(c):
            a = ri - origin[0]
            b = rj - origin[1]
            if 0 <= i - a < height and 0 <= j - b < width:
                res = max(res, int(src[i - a, j - b]) + se[ri, rj])

    if res > 255:
        return 255
    else:
        return res


def __dilation_b(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple):
    res = __dilation(src, se, i, j, origin)
    if 255 > res >= 0:
        return 0
    return res


def __erosion(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple):
    r, c = se.shape[:2]
    height, width = src.shape[:2]

    # Assume shape of src is larger that se
    res = 255
    for ri in range(r):
        for rj in range(c):
            a = ri - origin[0]
            b = rj - origin[1]
            if 0 <= i + a < height and 0 <= j + b < width:
                res = min(res, int(src[i + a, j + b]) - se[ri, rj])
    if res < 0:
        return 0
    else:
        return res


def __erosion_b(src: np.ndarray, se: np.ndarray, i: int, j: int, origin: tuple):
    res = __erosion(src, se, i, j, origin)
    if 255 >= res > 0:
        return 255
    return res


# Supports only two dimensional mat
def __join(l: np.ndarray, r: np.ndarray) -> np.ndarray:
    height, width = l.shape
    res = np.empty([height, width], l.dtype)
    for i in range(height):
        for j in range(width):
            res[i][j] = min(l[i][j], r[i][j])
    return res


if __name__ == "__main__":
    pass
