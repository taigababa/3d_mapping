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


def slide(map,dist,axis):
    map_ret = Hi_PROJECTION.make_3D_array(map.shape[1],map.shape[0],map.shape[2])
    for i in range(map.shape[2]):
        depth_image_refine = map[:,:,i]
        depth_image_shifted = np.roll(depth_image_refine,dist,axis=axis)
        map_ret[:,:,i] = depth_image_shifted
    return map_ret
