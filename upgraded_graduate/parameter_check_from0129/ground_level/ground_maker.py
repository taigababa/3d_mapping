#計算用モジュール
import numpy as np

#画像処理モジュール
import cv2
import math

import sys
#ファイルのパス名を利用するモジュール
import glob

import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import datetime
import os

#自作モジュール
import check as CHECK
import Projection as PROJECTION
import Show_3D_add as ADD
import Show_3D_color as Show_COLOR
import Hireso_projection as Hi_PROJECTION
import Gaussian_blur as FILTER
import Slide as SLIDE
import addition as ADDITION
import np_new_projection as NP

true_pic = cv2.imread("./output/front_input_calibrated.png")
x = true_pic.shape[1]
y = true_pic.shape[0]

for i in range(3):
    img = np.zeros((y,x,3), np.uint8)
    for n in range(50):
        mid = int(y/2)
        img[mid+n,:,:]= 255
    if i ==2:
        img[:,:,:] = 255
    path = "ground_img_" + str(i)+ ".png"
    cv2.imwrite(path,img)
