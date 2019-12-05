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
#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#切り取るスライスの深さ
depth = 57

def slice_img_viewer(y,map,name):
    map_stack = np.zeros((100,100)).reshape(100,100)
    for i in range(10):
        map_stack += map[:,x-5+i,:]

    ret, img_slice = cv2.threshold(map_stack, 0.5, 255, cv2.THRESH_BINARY_INV)
    CHECK.show_img(img_slice,name)
    CHECK.show_img(map_stack,name + "_non_thresh")

def ground_maker(map,depth):
    map_ground = np.ones((100,100)).reshape(100,100)
    map[depth,:,:] += map_ground





#fill_3D_array('IMG_0104_result.png',map_front,thresh,dist,mode)
#正面作成
#slideは0だと横方向(plot的に)
#slideは1だと縦方向(負の値だと上に動く)
#distが大きければ，広がり具合が増す
map_front = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0117_result.png',map_front,0,155,2,4,1,0)
map_front = SLIDE.slide(map_front,-3,1)

#Hi_PROJECTION.fill_3D_array_slide('IMG_0101_result.png',map_side,thresh,dist,mode,slide_dist,slide_mode,deg)
#slideは1だと横方向(plot的に)
#slideは0だと縦方向(正の値だと上に動く)
#横作成
map_side = Hi_PROJECTION.make_3D_array(y_range,z_range,x_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0118_result.png',map_side,0,130,2,-5,1,0)
map_side = SLIDE.slide(map_side,3,1)
map_side = np.flip(map_side.transpose(0,2,1),1)



#上作成
#0で上下(負の値で下)
#1で左右(負の値で右)
map_upper = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0114_result.png',map_upper,0,170,2,0,1,355)
#ここでずれの調節
map_upper = SLIDE.slide(map_upper,1,1)
map_upper = SLIDE.slide(map_upper,-7,0)
map_upper = np.flip(np.flip(np.flip(map_upper,2).transpose(2,0,1),0),2)
#map_upper = map_upper.transpose(0,2,1)
#map_upper = np.flip(map_upper,2)
map_upper = np.flip(map_upper,1)




map_true_add = map_front+map_side+map_upper
map_true = map_front*map_side*map_upper

map_front_side = map_front*map_side
map_add_front_side = map_front + map_side
map_check_upper = map_front_side+map_upper
#ADD.show_3D_3color(map_true_add)
#ADD.show_3D_3color(map_check_upper)
#ADD.show_3D_3color(map_add_front_side)
print('x=',map_true.shape[1],' y=',map_true.shape[0], ' z=',map_true.shape[2])

map_true_filtered = FILTER.Gaussian_blur_3D(map_true,3,0.3)
#Show_COLOR.show_3D_color(map_true_filtered,'pink',1)
#Show_COLOR.show_3D_color(map_front,'pink',1)
#Show_COLOR.show_3D_color(map_side,'pink',1)
#Show_COLOR.show_3D_color(map_upper,'pink',1)
#Show_COLOR.show_3D_color(map_front_side,'pink',1)

#CHECK.show_img(map_front[:,:,0])
#CHECK.show_img(map_side[:,99,:])
#CHECK.show_img(map_upper[50,:,:],'upper')
#CHECK.show_img(map_front_side[50,:,:],'front_side')
#CHECK.show_img(map_add_front_side[50,:,:],'front+side')

slice_img_front_side = map_add_front_side[depth,:,:]
#plt.imshow(slice_img_front_side, cmap='gray',interpolation='bicubic')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
#plt.show()

slice_img_upper = map_upper[depth,:,:]
#plt.imshow(slice_img_upper, cmap='gray',interpolation='bicubic')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
#plt.show()

overlap_checker = slice_img_upper + slice_img_front_side

map_for_check = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
map_for_check = map_true_filtered
ground_maker(map_for_check,depth)

place_checker = map_for_check[depth-1,:,:]
plt.imshow(overlap_checker, cmap='gray',interpolation='bicubic')
plt.grid(which='major',color='lime',linestyle='-')
plt.grid(which='minor',color='lime',linestyle='-')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
plt.show()

#測定用に0,255のグレー画像に変更


#z = depthでの位置
CHECK.show_img(place_checker,"place_checker")
#ここから各ねじの高さ測定(各重心座標の四捨五入した値で計算)
#1本目
x = 20
slice_img_viewer(x,map_true_filtered,"slice1")
slice_img_viewer(x,map_true_add/5,"add_slice_1")
#2
x = 30
slice_img_viewer(x,map_true_filtered,"slice2")
slice_img_viewer(x,map_true_add/5,"add_slice_2")
#3
x = 60
slice_img_viewer(x,map_true_filtered,"slice3")
slice_img_viewer(x,map_true_add/5,"add_slice_3")
#4
x = 90
slice_img_viewer(x,map_true_filtered,"slice4")
slice_img_viewer(x,map_true_add/5,"add_slice_4")
