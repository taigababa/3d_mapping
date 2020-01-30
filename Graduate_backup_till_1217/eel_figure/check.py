import cv2
import numpy as np





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

def show(fname):
    img = cv2.imread(fname)
    #ウィンドウの名前を設定
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    while(1):
        cv2.imshow("img", img)
        k = cv2.waitKey(1)
        #Escキーを押すと終了
        if k == 27:
            break
        #sを押すと結果を保存
        if k == ord("s"):
            cv2.imwrite(filename[:filename.rfind(".")] + "_result.png", result)
            break

def show_img(img,name):
    #ウィンドウの名前を設定
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    while(1):
        cv2.imshow("img", img)
        k = cv2.waitKey(1)
        #Escキーを押すと終了
        if k == 27:
            break
        #sを押すと結果を保存
        if k == ord("s"):
            cv2.imwrite(name+"_result.png", img*255)
            break
