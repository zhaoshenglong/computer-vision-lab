import cv2 as cv
import numpy as np


def robertOperator(src: np.ndarray):
    shape = src.shape
    dtype = src.dtype
    img: np.ndarray = np.empty(shape, dtype)
    for i in range(1, shape[0]):
        for j in range(1, shape[1]):
            t: int = np.abs(int(src[i][j]) - int(src[i - 1][j - 1])) + \
                     np.abs(int(src[i - 1][j]) - int(src[i][j - 1]))
            if t > 255:
                t = 255
            img[i][j] = np.uint8(t)

    # not deal with boundary
    for i in range(np.min(shape)):
        img[i][0] = src[i][0]
        img[0][i] = src[0][i]

    if shape[0] < shape[1]:
        for i in range(shape[0], shape[1]):
            img[shape[0] - 1][i] = src[shape[0] - 1][i]
    elif shape[0] > shape[1]:
        for i in range(shape[1], shape[0]):
            img[i][shape[1] - 1] = src[i][shape[1] - 1]
    else:
        pass
    return img


def sobelOperator(src: np.ndarray):
    shape = src.shape
    dtype = src.dtype
    img: np.ndarray = np.empty(shape, dtype)

    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            t: int = np.abs(int(src[i - 1][j - 1]) + (int(src[i][j - 1]) << 1) + int(src[i + 1][j - 1])
                            - int(src[i - 1][j + 1]) - (int(src[i][j + 1]) << 1) - int(src[i + 1][j + 1])) + \
                     np.abs(int(src[i - 1][j - 1]) + (int(src[i - 1][j]) << 1) + int(src[i - 1][j + 1])
                            - int(src[i + 1][j - 1]) - (int(src[i + 1][j]) << 1) - int(src[i + 1][j + 1]))
            if t > 255:
                t = 255
            img[i][j] = np.uint8(t)

    for i in range(shape[0]):
        img[i][0] = src[i][0]
        img[i][shape[1] - 1] = src[i][shape[1] - 1]
    for j in range(shape[1]):
        img[0][j] = src[0][j]
        img[shape[0] - 1][j] = src[shape[0] - 1][j]
    return img


def prewittOperator(src: np.ndarray):
    shape = src.shape
    dtype = src.dtype
    img: np.ndarray = np.empty(shape, dtype)

    for i in range(1, shape[0] - 1):
        for j in range(1, shape[1] - 1):
            t: int = np.abs(int(src[i - 1][j - 1]) + int(src[i][j - 1]) + int(src[i + 1][j - 1])
                            - int(src[i - 1][j + 1]) - int(src[i][j + 1]) - int(src[i + 1][j + 1])) + \
                     np.abs(int(src[i - 1][j - 1]) + int(src[i - 1][j]) + int(src[i - 1][j + 1])
                            - int(src[i + 1][j - 1]) - int(src[i + 1][j]) - int(src[i + 1][j + 1]))
            if t > 255:
                t = 255
            img[i][j] = np.uint8(t)

    for i in range(shape[0]):
        img[i][0] = src[i][0]
        img[i][shape[1] - 1] = src[i][shape[1] - 1]
    for j in range(shape[1]):
        img[0][j] = src[0][j]
        img[shape[0] - 1][j] = src[shape[0] - 1][j]
    return img


def main():
    img = cv.imread("../resource/lena.jpg", cv.IMREAD_GRAYSCALE)
    cv.imshow("source image", img)
    cv.imshow("roberts edge", robertOperator(img))
    cv.imshow("prewitt edge", prewittOperator(img))
    cv.imshow("sobel edge", sobelOperator(img))
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
