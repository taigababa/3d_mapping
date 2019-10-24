import cv2
import numpy as np
import slope_3D_mapping as map


def show(title,image):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def thresh(filename,threshold):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return gray

def thresh_img(img,threshold):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return gray

def convert(filename):
    img = cv2.imread(filename)
    hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
    return hsv



x_range = 100
y_range = 100
z_range = 100

threshold = 150

size = (100,100)
"""
img = cv2.imread('IMG_7885.JPG')
img_rotate = map.cut_rotate(img,(img.shape[0],img.shape[1]),40)
cv2.imwrite('rotate_pica.png',img_rotate)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
show('rotate',gray)
cv2.imwrite('threshold_pica.png',gray)

"""
"""
map_oblique = map.Make_3D_Array(y_range,x_range,z_range)
map.Fill_3D_Array('threshold_pica.png',map_oblique)
"""

"""
for i in range(z_range):
    slice = map_oblique[:,:,i]
    show('slice',slice)
"""
