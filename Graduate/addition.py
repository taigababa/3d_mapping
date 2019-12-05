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
import Gaussian_blur as FILTER
import Slide as SLIDE

def addition(map,shift):
    map_ret = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    for i in range(map.shape[2]):
        depth_image_refine = map[:,:,i]
        depth_image_shifted_x = np.roll(depth_image_refine,shift,axis=1)
        depth_image_shifted_x_minus = np.roll(depth_image_refine,-shift,axis=1)
        depth_image_shifted_y = np.roll(depth_image_refine,shift,axis=0)
        depth_image_shifted_y_minus = np.roll(depth_image_refine,-shift,axis=1)
        map_ret[:,:,i] = map[:,:,i]
        map_ret[:,:,i] += depth_image_shifted_x
        map_ret[:,:,i] += depth_image_shifted_y
        map_ret[:,:,i] += depth_image_shifted_y_minus
        map_ret[:,:,i] += depth_image_shifted_x_minus
    return map_ret
