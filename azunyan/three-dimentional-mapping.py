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
#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#カメラのパラメータ
#y = Ax + Bの形
A = 0.0008625821
B = 0.03849



#正面作成
map_front = PROJECTION.make_3D_array(y_range,x_range,z_range)
PROJECTION.fill_3D_array('IMG_0104_result.png',map_front,180,165,2)


#横作成
map_side = PROJECTION.make_3D_array(y_range,z_range,x_range)
PROJECTION.fill_3D_array('IMG_0101_result.png',map_side,167,123,2)
map_side = np.flip(map_side.transpose(0,2,1),1)



#上作成
map_upper = PROJECTION.make_3D_array(z_range,x_range,y_range)
PROJECTION.fill_3D_array('IMG_0103_result_result.png',map_upper,75,150,2)
map_upper = np.flip(np.flip(np.flip(map_upper,2).transpose(2,0,1),0),2)
map_upper = map_upper.transpose(0,2,1)
map_upper = np.flip(map_upper,2)
map_upper = np.flip(map_upper,1)



map_true_add = map_front+map_side+map_upper
map_true = map_front*map_side*map_upper

map_front_side = map_front*map_side
map_add_front_side = map_front + map_side
map_check_upper = map_front_side+map_upper
#ADD.show_3D_3color(map_true_add)
#ADD.show_3D_3color(map_check_upper)
#ADD.show_3D_3color(map_add_front_side)

Show_COLOR.show_3D_color(map_true,'pink',1)
#Show_COLOR.show_3D_color(map_front,'pink',1)
#Show_COLOR.show_3D_color(map_side,'pink',1)
#Show_COLOR.show_3D_color(map_upper,'pink',1)
#Show_COLOR.show_3D_color(map_front_side,'pink',1)

#CHECK.show_img(map_front[:,:,0])
#CHECK.show_img(map_side[:,99,:])
#CHECK.show_img(map_upper[50,:,:],'upper')
#CHECK.show_img(map_front_side[50,:,:],'front_side')
CHECK.show_img(map_add_front_side[50,:,:],'front+side')
