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
#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#切り取るスライスの深さ
depth = 62

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
        img[y-i,x-i] = [100,120,255]
        img[y-i,x] = [100,120,255]
        img[y-i,x+i] =[100,120,255]
        img[y,x-i] = [100,120,255]
        img[y,x] = [100,120,255]
        img[y,x+i] =[100,120,255]
        img[y+i,x-i] = [100,120,255]
        img[y+i,x] = [100,120,255]
        img[y+i,x+i] =[100,120,255]



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
#fill_3D_array('IMG_0104_result.png',map_front,thresh,dist,mode)
#正面作成
#slideは0だと横方向(plot的に)
#slideは1だと縦方向(負の値だと上に動く)
#distが大きければ，広がり具合が増す
map_front = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0117_result.png',map_front,0,163,2,4,1,0)
map_front = SLIDE.slide(map_front,-2,1)

#Hi_PROJECTION.fill_3D_array_slide('IMG_0101_result.png',map_side,thresh,dist,mode,slide_dist,slide_mode,deg)
#slideは1だと横方向(plot的に)
#slideは0だと縦方向(正の値だと上に動く)
#横作成
map_side = Hi_PROJECTION.make_3D_array(y_range,z_range,x_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0118_result.png',map_side,0,127,2,-5,1,0)
map_side = SLIDE.slide(map_side,3,1)
map_side = np.flip(map_side.transpose(0,2,1),1)

"""
#結果スライド用画像出力
map_side_to_show = Hi_PROJECTION.make_3D_array(y_range,z_range,x_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0118_result.png',map_side_to_show,0,127,2,0,1,0)
map_side_to_show = np.flip(map_side_to_show.transpose(1,2,0),1)
Show_COLOR.show_3D_color_nolabel(map_side_to_show,'black',1)
#結果出力ここまで
"""


#上作成
#0で上下(負の値で下)
#1で左右(負の値で右)
map_upper = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_0114_result.png',map_upper,0,178,2,0,1,355)
#ここでずれの調節
map_upper = SLIDE.slide(map_upper,1,1)
map_upper = SLIDE.slide(map_upper,-5,0)
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
map_true_additon = ADDITION.addition(map_true_filtered,0)
map_true_additon = FILTER.Gaussian_blur_3D(map_true_additon,3,0.3)
Show_COLOR.show_3D_color_nolabel(map_true_filtered,'black',1)
#Show_COLOR.show_3D_color(map_true_additon,'pink',1)
#Show_COLOR.show_3D_color(map_front,'pink',1)
#Show_COLOR.show_3D_color(map_side,'pink',1)
#Show_COLOR.show_3D_color(map_upper,'pink',1)
#Show_COLOR.show_3D_color(map_front_side,'pink',1)

#CHECK.show_img(map_front[:,:,0])
#CHECK.show_img(map_side[:,99,:])
#CHECK.show_img(map_upper[50,:,:],'upper')
#CHECK.show_img(map_front_side[50,:,:],'front_side')
#CHECK.show_img(map_add_front_side[50,:,:],'front+side')


#ここから断面系
"""
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
#ground_maker前にcheckしないとgroundで真っ白になる
place_checker = map_for_check[depth,:,:]
#z = depthでの位置
place_img_viewer_with_guide(depth,map_for_check,"place_with_guide")

ret, place_5 = cv2.threshold(map_true_filtered[58,:,:], 0.5, 255, cv2.THRESH_BINARY_INV)
CHECK.show_img(place_5,"place_for_5")




plt.imshow(overlap_checker, cmap='gray',interpolation='bicubic')
plt.grid(which='major',color='lime',linestyle='-')
plt.grid(which='minor',color='lime',linestyle='-')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
plt.show()

#測定用に0,255のグレー画像に変更

#ここから各ねじの高さ測定(各重心座標の四捨五入した値で計算)


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

#slice_img_viewer(x,map_true_add/5,"add_slice_4")

#横から見た図作成
view_from_side = np.zeros((100,100)).reshape(100,100)

for i in range(map_for_check.shape[1]):
    view_from_side += map_for_check[:,i,:]
ret, view_from_side_threshed = cv2.threshold(view_from_side, 0.5, 255, cv2.THRESH_BINARY_INV)
CHECK.show_img(view_from_side_threshed,"view_from_side")

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
"""
