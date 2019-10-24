import cv2
import numpy as np

def show(title,image):
    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread('pica.png')
size = (400,400)
center = (img.shape[0]/2, img.shape[1]/2)
rot_mat = cv2.getRotationMatrix2D(center, 40, 1.0)
#この移動がないと回転画像の左上からsize分切り取ってしまう
rot_mat[0][2] += -center[0]+size[0]/2 # -(元画像内での中心位置)+(切り抜きたいサイズの中心)
rot_mat[1][2] += -center[1]+size[1]/2 # 同上
rotate_img = cv2.warpAffine(img, rot_mat, size)
show('rotate',rotate_img)
#print(size)
