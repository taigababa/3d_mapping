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
depth = 25

#重ねる際のalpha
alpha = 0.0055

#fill_3D_array('IMG_0104_result.png',map_front,thresh,dist,mode)
#正面作成
#slideは0だと横方向(plot的に)
#slideは1だと縦方向(負の値だと上に動く)
map_front = Hi_PROJECTION.make_3D_array(y_range,x_range,z_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_8811_result.png',map_front,0,153,2,4,1,0)
map_front = SLIDE.slide(map_front,-1,1)

#Hi_PROJECTION.fill_3D_array_slide('IMG_0101_result.png',map_side,thresh,dist,mode,slide_dist,slide_mode,deg)
#slideは1だと横方向(plot的に)
#slideは0だと縦方向(正の値だと上に動く)
#横作成
map_side = Hi_PROJECTION.make_3D_array(y_range,z_range,x_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_8810_result.png',map_side,0,134,2,-5,1,0)
map_side = SLIDE.slide(map_side,3,1)
map_side = np.flip(map_side.transpose(0,2,1),1)



#上作成
#0で上下(負の値で下)
#1で左右(負の値で右)
map_upper = Hi_PROJECTION.make_3D_array(z_range,x_range,y_range)
Hi_PROJECTION.fill_3D_array_slide('IMG_8808_result.png',map_upper,0,104,2,0,1,85)
#ここでずれの調節
map_upper = SLIDE.slide(map_upper,1,1)
map_upper = SLIDE.slide(map_upper,-1,0)
map_upper = np.flip(np.flip(np.flip(map_upper,2).transpose(2,0,1),0),2)
#map_upper = map_upper.transpose(0,2,1)
#map_upper = np.flip(map_upper,2)
map_upper = np.flip(map_upper,1)




map_true_add = map_front+map_side+map_upper
map_true = map_front*map_side*map_upper

map_front_side = map_front*map_side
map_add_front_side = map_front + map_side
map_check_upper = map_front_side+map_upper
map_true_add_toshow = np.flip(np.flip(np.flip(map_true_add.transpose(1,2,0),2),1),0)
#ADD.show_3D_3color(map_true_add_toshow)
#ADD.show_3D_3color(map_check_upper)
map_add_front_side_toshow = np.flip(np.flip(np.flip(map_add_front_side.transpose(1,2,0),2),1),0)
#ADD.show_3D(map_add_front_side_toshow)
print('x=',map_true.shape[1],' y=',map_true.shape[0], ' z=',map_true.shape[2])

#ここでノイズならし
map_true_filtered = FILTER.Gaussian_blur_3D(map_true,3,0.3)

#ここから結果表示を整えるために軸入れ替え(x,z)
map_true_filtered_toshow = np.flip(np.flip(np.flip(map_true_filtered.transpose(1,2,0),2),1),0)
map_front_toshow = np.flip(np.flip(np.flip(map_front.transpose(1,2,0),2),1),0)
map_side_toshow = np.flip(np.flip(np.flip(map_side.transpose(1,2,0),2),1),0)
map_upper_toshow = np.flip(np.flip(np.flip(map_upper.transpose(1,2,0),2),1),0)

Show_COLOR.show_3D_color_3colors(map_front_toshow,'lime',alpha,map_side_toshow,'orange',alpha,map_upper_toshow,'crimson',alpha,map_true_filtered_toshow,'gray',0.3)



Show_COLOR.show_3D_color(map_true_filtered_toshow,'cyan',1)
Show_COLOR.show_3D_color(map_front_toshow,'lime',0.3)
Show_COLOR.show_3D_color(map_side_toshow,'orange',0.3)
Show_COLOR.show_3D_color(map_upper_toshow,'crimson',0.3)
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

plt.imshow(slice_img_upper, cmap='gray',interpolation='bicubic')
plt.grid(which='major',color='lime',linestyle='-')
plt.grid(which='minor',color='lime',linestyle='-')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
plt.show()

place_checker = map_true_filtered[depth,:,:]
plt.imshow(overlap_checker, cmap='gray',interpolation='bicubic')
plt.grid(which='major',color='lime',linestyle='-')
plt.grid(which='minor',color='lime',linestyle='-')
# plt.xticks([]), plt.yticks([])  #目盛りをなくす
plt.show()

#測定用に0,100のグレー画像に変更
ret, zslice = cv2.threshold(place_checker, 0.5, 255, cv2.THRESH_BINARY)


#CHECK.show_img(zslice,"z_slice50")
