import numpy as np
import cv2 as cv


def is_binary(src: np.ndarray) -> bool:
    for i in range(src.shape[0]):
        for j in range(src.shape[1]):
            if src[i][j] != 0 and src[i][j] != 255:
                return False
    return True


def main():
    img = cv.imread("../conditional_dilation.png", cv.IMREAD_GRAYSCALE)
    print(is_binary(img))
    ret, img = cv.threshold(img, 0, 255, cv.THRESH_OTSU)
    print(is_binary(img))
    cv.imshow("origin", img)
    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
