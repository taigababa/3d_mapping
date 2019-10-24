import cv2
import numpy as np


def Show(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# load image, change color spaces, and smoothing
img = cv2.imread('GardenEel_Kyoto.jpg')
width = img.shape[0]
height = img.shape[1]
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_HSV = cv2.GaussianBlur(img_HSV, (9, 9), 3)

img_blank = np.zeros((width, height, 3), np.uint8)
cv2.imwrite('Blank.jpg',img_blank)

#detect objects
img_H, img_S, img_V = cv2.split(img_HSV)
_thre, img_eels = cv2.threshold(img_H, 95, 255, cv2.THRESH_BINARY)
cv2.imwrite('eel_mask.jpg', img_eels)

# find objects
contours, hierarchy = cv2.findContours(img_eels, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

for i in range(0, len(contours)):
    if len(contours[i]) > 0:

        # remove small objects
        if cv2.contourArea(contours[i]) < 1000:
            continue
        if cv2.contourArea(contours[i]) > 50000:
            continue

#ブランクを初期化後抽出されたチンアナゴ描画

        cv2.polylines(img_blank, contours[i], True, (255, 255, 255), 5)
        filename = 'Detected_EEL_%d.jpg'%i
        print(filename)
        cv2.imwrite(filename,img_blank)
        img_blank = np.zeros((width, height, 3), np.uint8)




# save
cv2.imwrite('GardenEel_Kyoto_detected.jpg', img)
