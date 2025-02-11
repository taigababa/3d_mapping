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
import projection as PROJECTION

#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#カメラのパラメータ
#y = Ax + Bの形
A = 0.0008625821
B = 0.03849

#threshold用
threshold = 100

#正面作成
map_front = PROJECTION.make_3D_array(y_range,x_range,z_range)
PROJECTION.fill_3D_array(filename,map_front,threshold,dist)


#横作成
map_side = PROJECTION.make_3D_array(y_range,z_range,x_range)
PROJECTION.fill_3D_array(filename,map_side,threshold,dist)
map_side = np.flip(map_side,2).transpose(0,2,1)

#上作成
map_upper = PROJECTION.make_3D_array(z_range,x_range,y_range)
PROJECTION.fill_3D_array(filename,map_upper,threshold,dist)
map_upper = np.flip(map_upper,1).transpose(2,1,0)
