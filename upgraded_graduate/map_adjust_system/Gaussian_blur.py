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

#自作モジュール
import check as CHECK
import Projection as PROJECTION
import Show_3D_add as ADD
import Show_3D_color as Show_COLOR
import Hireso_projection as Hi_PROJECTION

def Gaussian_blur_3D(map,size,threshold_filter):
    map_return_x = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    map_return_y = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    map_return_z = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    map_return = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    for i in range(map.shape[0]):
        img = map[i,:,:]
        blurred_img = cv2.blur(img,ksize=(size,size))
        ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,1,cv2.THRESH_BINARY)
        map_return_y[i,:,:]=img_threshold

    for i in range(map.shape[1]):
        img = map[:,i,:]
        blurred_img = cv2.blur(img,ksize=(size,size))
        ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,1,cv2.THRESH_BINARY)
        map_return_x[:,i,:]=img_threshold

    for i in range(map.shape[2]):
        img = map[:,:,i]
        blurred_img = cv2.blur(img,ksize=(size,size))
        ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,1,cv2.THRESH_BINARY)
        map_return_z[:,:,i]=img_threshold

    map_return = map_return_x + map_return_y + map_return_z
    map_return /=3
    return map_return
