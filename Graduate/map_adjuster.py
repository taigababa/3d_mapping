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
import addition as ADDITION
import np_new_projection as NP

#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#トラックバー用グローバル変数
#切り取るスライスの深さ
depth = 0
front_dist = 100
side_dist = 100
upper_dist = 100
front_deg = 0
side_deg = 0
upper_deg = 0
map_front = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_side = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_upper = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_true = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_true_filtered = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)




"""
#コールバック関数設定ゾーン
def nothing(x):
    pass
#windowとimgを設定しないとトラックバーを作れない
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
#cv2.createTrackbar("trackbar_name","window_name",min,max,呼び出す関数)
cv2.createTrackbar("depth", "image", 0, 99, nothing)
# create switch for ON/OFF functionality
switch = '0 : front \n1 : side\n2 : upper\n3 : filtered'
cv2.createTrackbar(switch, 'image',0,3,nothing)
cv2.createTrackbar("front_dist","image",100,300,nothing)
cv2.createTrackbar("side_dist","image",100,300,nothing)
cv2.createTrackbar("upper_dist","image",100,300,nothing)
cv2.createTrackbar("front_deg","image",0,360,nothing)
cv2.createTrackbar("side_deg","image",0,360,nothing)
cv2.createTrackbar("upper_deg","image",0,360,nothing)
"""
#front
map_front = NP.make_map('IMG_0116_result_invert.png',0,front_dist,0,front_deg)
#side
map_side = NP.make_map_side('IMG_0118_result.png',0,side_dist,0,side_deg)
#upper
map_upper = NP.make_map_upper('IMG_0114_inputver_result.png',0,upper_dist,0,upper_deg)
Show_COLOR.show_3D_color_nolabel(map_front,'black',1)
Show_COLOR.show_3D_color_nolabel(map_side,'black',1)
Show_COLOR.show_3D_color_nolabel(map_upper,'black',1)

"""
#ここからwindow処理
while(1):
    cv2.imshow("image", img)
    k = cv2.waitKey(1)
    #escキーで終了
    if k == 27:
        print('no save')
        break
    depth = cv2.getTrackbarPos('depth','image')
    map_select = cv2.getTrackbarPos(switch,'image')
    if map_select==0:
        map = map_front
    elif map_select==1:
        map = map_side
    elif map_select==2:
        map = map_upper
    elif map_select==3:
        map = map_true_filtered
    front_dist = cv2.getTrackbarPos("front_dist","image")
    side_dist = cv2.getTrackbarPos("side_dist","image")
    upper_dist = cv2.getTrackbarPos("upper_dist","image")
    front_deg = cv2.getTrackbarPos("front_deg","image")
    side_deg = cv2.getTrackbarPos("side_deg","image")
    upper_deg = cv2.getTrackbarPos("upper_deg","image")
    #front
    map_front = NP.make_map('IMG_0116_result_invert.png',0,front_dist,0,front_deg)
    #side
    map_side = NP.make_map_side('IMG_0118_result.png',0,side_dist,0,side_deg)
    #upper
    map_upper = NP.make_map_upper('IMG_0114_inputver_result.png',0,upper_dist,0,upper_deg)
    #map積算
    map_true = map_front*map_side*map_upper
    #mapフィルターがけ
    map_true_filtered = FILTER.Gaussian_blur_3D(map_true,3,0.3)
    img = map[depth,:,:]

    #whileここまで
"""
