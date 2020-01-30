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
#初期化
map_front = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_side = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_upper = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_true = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_true_filtered = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
map_front_side = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
#設定値
depth = 51
front_dist = 153
front_deg = 2
front_move_x = 6
front_move_y = 10

side_dist = 119
side_deg = 1
side_move_x = 7
side_move_y = 10

upper_dist = 188
upper_deg = 180
upper_move_x = 15
upper_move_y = 7

guide_color = [100,120,255]



def slice_img_viewer(x,map,name):
    map_stack = np.zeros((100,100)).reshape(100,100)
    for i in range(10):
        map_stack += map[:,x-5+i,:]

    ret, img_slice = cv2.threshold(map_stack, 0.5, 255, cv2.THRESH_BINARY_INV)
    CHECK.show_img(img_slice,name)
    #CHECK.show_img(map_stack,name + "_non_thresh")

def place_img_viewer(y,map,name):
    map_stack = np.zeros((100,100)).reshape(100,100)
    for i in range(20):
        map_stack += map[y-10+i,:,:]

    ret, img_slice = cv2.threshold(map_stack, 0.5, 255, cv2.THRESH_BINARY_INV)
    CHECK.show_img(img_slice,name)


def ground_maker(map,depth):
    map_with_ground = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
    map_ground = np.ones((100,100)).reshape(100,100)
    map_with_ground = map
    map_with_ground[depth,:,:] += map_ground
    return map_with_ground

def guide_maker(img,x,y,rad):
    for i in range(rad):
        img[y-i,x-i] = guide_color
        img[y-i,x] = guide_color
        img[y-i,x+i] =guide_color
        img[y,x-i] = guide_color
        img[y,x] = guide_color
        img[y,x+i] =guide_color
        img[y+i,x-i] = guide_color
        img[y+i,x] = guide_color
        img[y+i,x+i] =guide_color



def guideline(img):
    guide = img
    guide_maker(guide,80,20,3)
    guide_maker(guide,30,30,3)
    guide_maker(guide,50,30,3)
    guide_maker(guide,30,60,3)
    guide_maker(guide,70,60,3)
    guide_maker(guide,10,90,3)
    return guide

def place_img_viewer_with_guide(y,map,name):
    map_stack = np.zeros((100,100)).reshape(100,100)
    for i in range(20):
        map_stack += map[y-10+i,:,:]


    ret, img_slice = cv2.threshold(map_stack, 0.5, 255, cv2.THRESH_BINARY_INV)
    #guide = guideline()
    #guide *= 80
    #img_slice += guide
    img_slice = img_slice.astype(np.uint8)
    img_slice_color = cv2.cvtColor(img_slice, cv2.COLOR_GRAY2BGR)
    img_slice_color = guideline(img_slice_color)

    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    while(1):
        cv2.imshow("img", img_slice_color)
        k = cv2.waitKey(1)
        #Escキーを押すと終了
        if k == 27:
            break
        #sを押すと結果を保存
        if k == ord("s"):
            cv2.imwrite(name+"_result.png", img_slice_color)
            break

def min_tracker(img):
    input = np.array(img)
    black = np.where(input < 0)
    print("y_min" + min(black[0]) + ",x_min" + min(black[1]))



#ここから本文

map_front = NP.make_map('front_input.png',0,front_dist,0)
#x軸(左右)移動
map_front = SLIDE.slide_front(map_front,front_move_y-10,1)
#y軸(上下)移動
map_front = SLIDE.slide_front(map_front,front_move_x-10,0)
#回転
map_front = NP.Rotate_front(map_front,front_deg)
#side
map_side = NP.make_map_side('side_input.png',0,side_dist,0)
#x軸(左右)移動
map_side = SLIDE.slide_side(map_side,side_move_y-10,1)
#y軸(上下)移動
map_side = SLIDE.slide_side(map_side,side_move_x-10,0)
#回転
map_side = NP.Rotate_side(map_side, side_deg)
#upper
map_upper = NP.make_map_upper('upper_input.png',0,upper_dist,upper_deg)
#x軸(左右)移動
map_upper = SLIDE.slide_upper(map_upper,upper_move_y-10,0)
#y軸(上下)移動
map_upper = SLIDE.slide_upper(map_upper,upper_move_x-10,1)
#map積算
map_true = map_front*map_side*map_upper
#mapフィルターがけ
map_true_filtered = FILTER.Gaussian_blur_3D(map_true,3,0.3)
map_true_added = map_front + map_side + map_upper
map_front_side = map_front + map_side

map_for_check = map_true_filtered



#1本目
x = 20
slice_img_viewer(x,map_for_check,"slice1")

#slice_img_viewer(x,map_true_add/5,"add_slice_1")
#2
x = 30
slice_img_viewer(x,map_for_check,"slice2")
#slice_img_viewer(x,map_true_add/5,"add_slice_2")
#3
x = 60
slice_img_viewer(x,map_for_check,"slice3")
#slice_img_viewer(x,map_true_add/5,"add_slice_3")
#4
x = 90
slice_img_viewer(x,map_for_check,"slice4")


map_with_ground = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
map_with_ground = ground_maker(map_for_check,depth)
#2
x=30
slice_img_viewer(x,map_with_ground,"slice2_ground")

#3
x = 60
slice_img_viewer(x,map_with_ground,"slice3_ground")


#1
x = 20
slice_img_viewer(x,map_with_ground,"slice1_ground")
#4
x = 90
slice_img_viewer(x,map_with_ground,"slice4_ground")
