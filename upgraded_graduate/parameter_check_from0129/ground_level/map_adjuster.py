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

#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100
#グリッド間隔
x_step = 10
y_step = 10
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
map_front_side = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_for_check = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)

#関数設定



#コールバック関数設定ゾーン
def nothing(x):
    pass
#windowとimgを設定しないとトラックバーを作れない
img = np.zeros((300,512,3), np.uint8)
img_true = np.zeros((300,512,3), np.uint8)

#トラックバー用windowの設計
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
#画像用windowの設計
cv2.namedWindow("image_show",cv2.WINDOW_NORMAL)
#map_true用windowの設計
cv2.namedWindow("image_true",cv2.WINDOW_NORMAL)
#cv2.createTrackbar("trackbar_name","window_name",min,max,呼び出す関数)
cv2.createTrackbar("depth", "image", 59, 99, nothing)
cv2.createTrackbar("x_axis","image",60,99,nothing)
# create switch for ON/OFF functionality
switch = '0 : front \n1 : side\n2 : upper\n3 : filtered\n4 : added\n5 : front+side'
cv2.createTrackbar(switch, 'image',3,5,nothing)
switch_guide = '0 : no guide \n1 : guideline'
cv2.createTrackbar(switch_guide, 'image',1,1,nothing)
switch_ground = '0 : no ground \n1 : ground'
cv2.createTrackbar(switch_ground, 'image',1,1,nothing)
cv2.createTrackbar("front_dist","image",50,300,nothing)
cv2.createTrackbar("front_deg","image",0,360,nothing)
cv2.createTrackbar("front_move_y","image",10,20,nothing)
cv2.createTrackbar("front_move_x","image",10,20,nothing)
cv2.createTrackbar("front_move_z","image",10,20,nothing)

cv2.createTrackbar("side_dist","image",50,300,nothing)
cv2.createTrackbar("side_deg","image",0,360,nothing)
cv2.createTrackbar("side_move_y","image",10,20,nothing)
cv2.createTrackbar("side_move_x","image",10,20,nothing)

cv2.createTrackbar("upper_dist","image",400,500,nothing)
cv2.createTrackbar("upper_deg","image",180,360,nothing)
cv2.createTrackbar("upper_move_y","image",14,20,nothing)
cv2.createTrackbar("upper_move_x","image",8,20,nothing)
"""
#front
map_front = NP.make_map('front_input.png',0,front_dist,front_deg)
#side
map_side = NP.make_map_side('side_input.png',0,side_dist,side_deg)
#upper
map_upper = NP.make_map_upper('upper_input.png',0,upper_dist,upper_deg)


Show_COLOR.show_3D_color_nolabel(map_front,'black',1)
Show_COLOR.show_3D_color_nolabel(map_side,'black',1)
Show_COLOR.show_3D_color_nolabel(map_upper,'black',1)

"""
#ここからwindow処理
while(1):

    cv2.imshow("image_show", img)
    cv2.imshow("image_true",img_true)


    k = cv2.waitKey(1)
    #escキーで終了
    if k == 27:
        print('no save')
        break
    #sを押すと結果を保存
    if k == ord("s"):
        ret, img_reverse = cv2.threshold(img, 0.5, 255, cv2.THRESH_BINARY_INV)
        dt_now = datetime.datetime.now()
        path = dt_now.strftime('%Y:%m:%d:%H:%M:%S')
        if ground_select==0:
            cv2.imwrite(path + "depth="+str(depth)+"_place.png", img_reverse*255)
        elif ground_select==1:
            cv2.imwrite(path + "x-axis="+str(x_axis)+"_height.png",img_reverse*255)
        continue
    #eを押すとパラメータ設定を保存
    if k== ord("e"):
        #日付取得
        dt_now = datetime.datetime.now()
        path = dt_now.strftime('%Y:%m:%d:%H:%M:%S')+".txt"
        with open(path,mode='w') as f:
            f.write(str(front_dist))
            f.write(",")
            f.write(str(front_deg))
            f.write(",")
            f.write(str(front_move_x))
            f.write(",")
            f.write(str(front_move_y))
            f.write(",")

            f.write(str(side_dist))
            f.write(",")
            f.write(str(side_deg))
            f.write(",")
            f.write(str(side_move_x))
            f.write(",")
            f.write(str(side_move_y))
            f.write(",")

            f.write(str(upper_dist))
            f.write(",")
            f.write(str(upper_deg))
            f.write(",")
            f.write(str(upper_move_x))
            f.write(",")
            f.write(str(upper_move_y))
            f.write(",")



    depth = cv2.getTrackbarPos('depth','image')
    x_axis = cv2.getTrackbarPos('x_axis','image')
    map_select = cv2.getTrackbarPos(switch,'image')
    if map_select==0:
        map = map_front
    elif map_select==1:
        map = map_side
    elif map_select==2:
        map = map_upper
    elif map_select==3:
        map = map_true_filtered
    elif map_select==4:
        map = map_true_added
    elif map_select==5:
        map = map_front_side

    front_dist = cv2.getTrackbarPos("front_dist","image")
    side_dist = cv2.getTrackbarPos("side_dist","image")
    upper_dist = cv2.getTrackbarPos("upper_dist","image")
    front_deg = cv2.getTrackbarPos("front_deg","image")
    side_deg = cv2.getTrackbarPos("side_deg","image")
    upper_deg = cv2.getTrackbarPos("upper_deg","image")
    front_move_x = cv2.getTrackbarPos("front_move_x","image")
    front_move_y = cv2.getTrackbarPos("front_move_y","image")
    front_move_z = cv2.getTrackbarPos("front_move_z","image")
    side_move_x = cv2.getTrackbarPos("side_move_x","image")
    side_move_y = cv2.getTrackbarPos("side_move_y","image")
    upper_move_x = cv2.getTrackbarPos("upper_move_x","image")
    upper_move_y = cv2.getTrackbarPos("upper_move_y","image")

    #front
    map_front = NP.make_map('ground_img_0.png',0,front_dist,0)
    #x軸(左右)移動
    map_front = SLIDE.slide_front(map_front,front_move_y-10,1)
    #y軸(上下)移動
    map_front = SLIDE.slide_front(map_front,front_move_x-10,0)
    #回転
    map_front = NP.Rotate_front(map_front,front_deg)
    #z軸移動(サイドとの高さ合わせ)
    map_front = SLIDE.slide_front_z(map_front,front_move_z-10)
    #side
    map_side = NP.make_map_side('ground_img_1.png',0,side_dist,0)
    #x軸(左右)移動
    map_side = SLIDE.slide_side(map_side,side_move_y-10,1)
    #y軸(上下)移動
    map_side = SLIDE.slide_side(map_side,side_move_x-10,0)
    #回転
    map_side = NP.Rotate_side(map_side, side_deg)
    #upper
    map_upper = NP.make_map_upper('ground_img_2.png',0,upper_dist,upper_deg)
    #x軸(左右)移動
    map_upper = SLIDE.slide_upper(map_upper,upper_move_y-10,0)
    #y軸(上下)移動
    map_upper = SLIDE.slide_upper(map_upper,upper_move_x-10,1)
    #map積算
    map_true = map_front*map_side*map_upper
    #mapフィルターがけ
    map_true_filtered = FILTER.Gaussian_blur_3D(map_true,3,0.4)
    map_true_added = map_front + map_side + map_upper
    map_front_side = map_front + map_side



    ground_select = cv2.getTrackbarPos(switch_ground,'image')
    if ground_select==0:
        img = map[depth,:,:]

    elif ground_select==1:
        img = map[:,x_axis,:]
        for n in range(3):
            img += map[:,x_axis-n+2,:]
        img[depth,:] += 1

    guide_select = cv2.getTrackbarPos(switch_guide,'image')
    if guide_select==0:
        continue
    elif guide_select==1:
        #オブジェクトimgのshapeメソッドの1つ目の戻り値(画像の高さ)をimg_yに、2つ目の戻り値(画像の幅)をimg_xに
        img_y,img_x=img.shape[:2]
        #横線を引く：y_stepからimg_yの手前までy_stepおきに白い(BGRすべて255)横線を引く
        img[y_step:img_y:y_step,:]= 255
        #縦線を引く：x_stepからimg_xの手前までx_stepおきに白い(BGRすべて255)縦線を引く
        img[:, x_step:img_x:x_step] = 255



    img_true = map_true_filtered[depth,:,:]
    img_true_y,img_true_x=img_true.shape[:2]
    #横線を引く：y_stepからimg_yの手前までy_stepおきに白い(BGRすべて255)横線を引く
    img_true[y_step:img_true_y:y_step,:]= 255
    #縦線を引く：x_stepからimg_xの手前までx_stepおきに白い(BGRすべて255)縦線を引く
    img_true[:, x_step:img_true_x:x_step] = 255





    #whileここまで
Show_COLOR.show_heat_color_nolabel(map_true_filtered,"black",1)
