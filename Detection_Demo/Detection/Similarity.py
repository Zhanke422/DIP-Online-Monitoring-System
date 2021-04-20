import cv2


def similarity(image1, image2):
    degree = 0
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + \
                (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree

if __name__ == "__main__":
    p1=cv2.imread("test1.png")
    p2=cv2.imread("test2.png")
    similarity(p1,p2)