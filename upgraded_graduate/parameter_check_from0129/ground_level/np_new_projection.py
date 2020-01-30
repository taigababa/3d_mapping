#計算用モジュール
import numpy as np

#画像処理モジュール
import cv2

import sys
#ファイルのパス名を利用するモジュール
import glob

import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors

#計算用
import math

#自作
import check

#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100




#カメラのパラメータ[mm/pixel]
#y = Ax + Bの形
A = 0.0008625821
B = 0.03849


"""
#カメラのパラメータ[mm/pixel]
#200*200*200用
#y = Ax + Bの形
A = 0.00043129
B = 0.019245
"""

#threshold用
threshold = 0

#フィルタ設定
w = 3
h = 3
threshold_filter = 0.3

size = 3

#3次元配列作成関数
def make_3D_array(y,x,z):
    #array上での次元と座標系ではx,yが入れ替わる
    array_3D = np.zeros((y,x,z)).reshape(y,x,z)

    return array_3D



#3次元配列入力関数
#filenameで写真選択(''付き)
#arrayでmap_???を指定
#thresholdは値
#distは距離[mm]
#styleはh_img,s_img.v_imgのいずれかを指定(r=0,g=1,b=2)
def make_map(filename,threshold,dist,degree):
    array = make_3D_array(y_range,x_range,z_range)
    x = array.shape[1]
    y = array.shape[0]
    z = array.shape[2]
    images = glob.glob(filename)
    try:
        for fname in images:
            img = cv2.imread(fname)
            #元画像のx取得
            im_height = img.shape[0]
            im_width = img.shape[1]
            _, gray = cv2.threshold(img, threshold, 255,cv2.THRESH_BINARY_INV )
            #01に変換
            gray = gray/255
            #フィルタぼかし
            blurred_img = cv2.blur(gray,ksize=(w,h))
            #あらためて二値化
            ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,255,cv2.THRESH_BINARY_INV)
            img_threshold /=255
            #check.show_img(img_threshold,'threshold')
            #ここから回転
            img_rotated = cut_rotate(img_threshold,(img_threshold.shape[1],img_threshold.shape[0]),degree)
            #check.show_img(img_rotated,'rotate')
            img_rotate = img_rotated[:,:,0]
            #cv2.imwrite("front_inputed.png",img_rotate*255)
            #check.show_img(img_rotate,'rotate')
            #ここからz軸に対してスライス(xy平面)ごとに入力
            for depth_frame in range(z):

                #変形倍率convの計算
                conv = (A*(dist + depth_frame) - B)
                #depth_imageはそのdepthでの実サイズ画像
                depth_image = cv2.resize(img_rotate, (int(im_width*conv), int(im_height*conv)))
                #check.show_img(depth_image,'rotate')


                #ここからサイズ調節
                ysize = depth_image.shape[0]


                #縦方向引き伸ばし
                if ysize <= y:
                    #print('y_upgrade')
                    y_change = y - ysize
                    y_change_0 = int(np.floor(y_change/2))
                    round_checker_y = y_change/2 - y_change_0
                    #roundではやばそうなので丁寧の処理
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0

                    #print(y_change_0,y_change_max)
                    refine_y_0_array = np.zeros((y_change_0, depth_image.shape[1]))

                    refine_y_max_array = np.zeros((y_change_max, depth_image.shape[1]))


                    depth_image_refine = np.vstack((refine_y_0_array,depth_image))
                    depth_image_refine = np.vstack((depth_image_refine, refine_y_max_array))
                    #print('add y refine',depth_image_refine.shape[0],depth_frame)

                #縦方向削るパターン
                elif ysize > y:
                    #print('reduce',depth_image.shape[0])
                    y_change = ysize - y
                    #floorは切り捨て
                    y_change_0 = int(np.floor(y_change/2))
                    #print('y_change',y_change)
                    #print('y_change_0',y_change_0)
                    round_checker_y = y_change/2 - y_change_0
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0
                    #print('y_change_max',y_change_max)
                    depth_image_refine_0 = np.delete(depth_image, np.s_[:y_change_0], 0)
                    #print('after 0 refine',depth_image_refine_0.shape[0])
                    depth_image_refine = np.delete(depth_image_refine_0, np.s_[depth_image_refine_0.shape[0] - y_change_max:], 0)
                    #print('after max refine',depth_image_refine.shape[0])

                #横方向変化
                #横方向引き伸ばし
                #x軸方向の変化を求める(100より少ないケース)
                if depth_image_refine.shape[1] <= x:
                    #print('upgrade')
                    x_change = x - depth_image_refine.shape[1]
                    x_change_0 = int(np.floor(x_change/2))
                    round_checker = x_change/2 - x_change_0
                    #四捨五入はroundだとバグりそうなので
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0


                    refine_x_0_array = np.zeros((y,x_change_0))

                    refine_x_max_array = np.zeros((y, x_change_max))


                    depth_image_refine = np.hstack((refine_x_0_array,depth_image_refine))
                    depth_image_refine = np.hstack((depth_image_refine, refine_x_max_array))
                    #print('add x refine',depth_image_refine.shape[1])

                #x軸調整(100より多いケース)
                elif depth_image_refine.shape[1] > x:
                    #print('reduce',depth_image_refine.shape[1])
                    x_change = depth_image_refine.shape[1] - x
                    x_change_0 = int(np.floor(x_change/2))
                    #print('x_change_0',x_change_0)
                    round_checker = x_change/2 - x_change_0
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0

                    depth_image_refine = np.delete(depth_image_refine, np.s_[:x_change_0], 1)
                    #print('after 0 refine',depth_image_refine.shape[1])
                    depth_image_refine = np.delete(depth_image_refine, np.s_[depth_image_refine.shape[1] - x_change_max:], 1)
                    #print('after max refine', depth_image_refine.shape[1],depth_frame)

                #ここから配列入力
                #の前にもう一度2値化
                depth_image_filtered = cv2.blur(depth_image_refine,ksize=(size,size))
                _,depth_image_for_input = cv2.threshold(depth_image_refine, 0.3, 255,cv2.THRESH_BINARY)
                array[:,:,depth_frame]= depth_image_for_input
            return array


    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #make_map関数ここまで

def make_map_side(filename,threshold,dist,degree):
    array = make_3D_array(y_range,x_range,z_range)
    x = array.shape[1]
    y = array.shape[0]
    z = array.shape[2]
    images = glob.glob(filename)
    try:
        for fname in images:
            img = cv2.imread(fname)
            #元画像のx取得
            im_height = img.shape[0]
            im_width = img.shape[1]
            _, gray = cv2.threshold(img, threshold, 255,cv2.THRESH_BINARY_INV )
            #01に変換
            gray = gray/255
            #フィルタぼかし
            blurred_img = cv2.blur(gray,ksize=(w,h))
            #あらためて二値化
            ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,255,cv2.THRESH_BINARY_INV)
            img_threshold /=255
            #ここから回転
            img_rotated = cut_rotate(img_threshold,(img_threshold.shape[1],img_threshold.shape[0]),degree)
            img_rotate = img_rotated[:,:,0]
            #check.show_img(img_rotate_to_show,"after_processing")
            #cv2.imwrite("side_inputed.png",img_rotate*255)
            for depth_frame in range(z):

                #変形倍率convの計算
                conv = (A*(dist + depth_frame) - B)
                #depth_imageはそのdepthでの実サイズ画像
                depth_image = cv2.resize(img_rotate, (int(im_width*conv), int(im_height*conv)))


                #ここからサイズ調節
                ysize = depth_image.shape[0]


                #縦方向引き伸ばし
                if ysize <= y:
                    #print('y_upgrade')
                    y_change = y - ysize
                    y_change_0 = int(np.floor(y_change/2))
                    round_checker_y = y_change/2 - y_change_0
                    #roundではやばそうなので丁寧の処理
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0

                    #print(y_change_0,y_change_max)
                    refine_y_0_array = np.zeros((y_change_0, depth_image.shape[1]))

                    refine_y_max_array = np.zeros((y_change_max, depth_image.shape[1]))


                    depth_image_refine = np.vstack((refine_y_0_array,depth_image))
                    depth_image_refine = np.vstack((depth_image_refine, refine_y_max_array))
                    #print('add y refine',depth_image_refine.shape[0],depth_frame)

                #縦方向削るパターン
                elif ysize > y:
                    #print('reduce',depth_image.shape[0])
                    y_change = ysize - y
                    #floorは切り捨て
                    y_change_0 = int(np.floor(y_change/2))
                    #print('y_change',y_change)
                    #print('y_change_0',y_change_0)
                    round_checker_y = y_change/2 - y_change_0
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0
                    #print('y_change_max',y_change_max)
                    depth_image_refine_0 = np.delete(depth_image, np.s_[:y_change_0], 0)
                    #print('after 0 refine',depth_image_refine_0.shape[0])
                    depth_image_refine = np.delete(depth_image_refine_0, np.s_[depth_image_refine_0.shape[0] - y_change_max:], 0)
                    #print('after max refine',depth_image_refine.shape[0])

                #横方向変化
                #横方向引き伸ばし
                #x軸方向の変化を求める(100より少ないケース)
                if depth_image_refine.shape[1] <= x:
                    #print('upgrade')
                    x_change = x - depth_image_refine.shape[1]
                    x_change_0 = int(np.floor(x_change/2))
                    round_checker = x_change/2 - x_change_0
                    #四捨五入はroundだとバグりそうなので
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0


                    refine_x_0_array = np.zeros((y,x_change_0))

                    refine_x_max_array = np.zeros((y, x_change_max))


                    depth_image_refine = np.hstack((refine_x_0_array,depth_image_refine))
                    depth_image_refine = np.hstack((depth_image_refine, refine_x_max_array))
                    #print('add x refine',depth_image_refine.shape[1])

                #x軸調整(100より多いケース)
                elif depth_image_refine.shape[1] > x:
                    #print('reduce',depth_image_refine.shape[1])
                    x_change = depth_image_refine.shape[1] - x
                    x_change_0 = int(np.floor(x_change/2))
                    #print('x_change_0',x_change_0)
                    round_checker = x_change/2 - x_change_0
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0

                    depth_image_refine = np.delete(depth_image_refine, np.s_[:x_change_0], 1)
                    #print('after 0 refine',depth_image_refine.shape[1])
                    depth_image_refine = np.delete(depth_image_refine, np.s_[depth_image_refine.shape[1] - x_change_max:], 1)
                    #print('after max refine', depth_image_refine.shape[1],depth_frame)

                #ここから配列入力
                depth_image_filtered = cv2.blur(depth_image_refine,ksize=(size,size))
                _,depth_image_for_input = cv2.threshold(depth_image_refine, 0.4, 255,cv2.THRESH_BINARY)
                array[:,:,depth_frame]= depth_image_for_input
            array = np.flip(array.transpose(0,2,1),1)
            return array


    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #make_map_side関数ここまで

def make_map_upper(filename,threshold,dist,degree):
    array = make_3D_array(y_range,x_range,z_range)
    x = array.shape[1]
    y = array.shape[0]
    z = array.shape[2]
    images = glob.glob(filename)
    try:
        for fname in images:
            img = cv2.imread(fname)
            #元画像のx取得
            im_height = img.shape[0]
            im_width = img.shape[1]
            _, gray = cv2.threshold(img, threshold, 255,cv2.THRESH_BINARY_INV )
            #01に変換
            gray = gray/255
            #フィルタぼかし
            blurred_img = cv2.blur(gray,ksize=(w,h))
            #あらためて二値化
            ret,img_threshold = cv2.threshold(blurred_img,threshold_filter,255,cv2.THRESH_BINARY_INV)
            img_threshold /=255
            #ここから回転
            img_rotated = cut_rotate(img_threshold,(img_threshold.shape[1],img_threshold.shape[0]),degree)
            img_rotate = img_rotated[:,:,0]
            #cv2.imwrite("upper_inputed.png",img_rotate*255)



            #ここからz軸に対してスライス(xy平面)ごとに入力

            for depth_frame in range(z):

                #変形倍率convの計算
                conv = (A*(dist + depth_frame) - B)
                #depth_imageはそのdepthでの実サイズ画像
                depth_image = cv2.resize(img_rotate, (int(im_width*conv), int(im_height*conv)))


                #ここからサイズ調節
                ysize = depth_image.shape[0]


                #縦方向引き伸ばし
                if ysize <= y:
                    #print('y_upgrade')
                    y_change = y - ysize
                    y_change_0 = int(np.floor(y_change/2))
                    round_checker_y = y_change/2 - y_change_0
                    #roundではやばそうなので丁寧の処理
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0

                    #print(y_change_0,y_change_max)
                    refine_y_0_array = np.zeros((y_change_0, depth_image.shape[1]))

                    refine_y_max_array = np.zeros((y_change_max, depth_image.shape[1]))


                    depth_image_refine = np.vstack((refine_y_0_array,depth_image))
                    depth_image_refine = np.vstack((depth_image_refine, refine_y_max_array))
                    #print('add y refine',depth_image_refine.shape[0],depth_frame)

                #縦方向削るパターン
                elif ysize > y:
                    #print('reduce',depth_image.shape[0])
                    y_change = ysize - y
                    #floorは切り捨て
                    y_change_0 = int(np.floor(y_change/2))
                    #print('y_change',y_change)
                    #print('y_change_0',y_change_0)
                    round_checker_y = y_change/2 - y_change_0
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0
                    #print('y_change_max',y_change_max)
                    depth_image_refine_0 = np.delete(depth_image, np.s_[:y_change_0], 0)
                    #print('after 0 refine',depth_image_refine_0.shape[0])
                    depth_image_refine = np.delete(depth_image_refine_0, np.s_[depth_image_refine_0.shape[0] - y_change_max:], 0)
                    #print('after max refine',depth_image_refine.shape[0])

                #横方向変化
                #横方向引き伸ばし
                #x軸方向の変化を求める(100より少ないケース)
                if depth_image_refine.shape[1] <= x:
                    #print('upgrade')
                    x_change = x - depth_image_refine.shape[1]
                    x_change_0 = int(np.floor(x_change/2))
                    round_checker = x_change/2 - x_change_0
                    #四捨五入はroundだとバグりそうなので
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0


                    refine_x_0_array = np.zeros((y,x_change_0))

                    refine_x_max_array = np.zeros((y, x_change_max))


                    depth_image_refine = np.hstack((refine_x_0_array,depth_image_refine))
                    depth_image_refine = np.hstack((depth_image_refine, refine_x_max_array))
                    #print('add x refine',depth_image_refine.shape[1])

                #x軸調整(100より多いケース)
                elif depth_image_refine.shape[1] > x:
                    #print('reduce',depth_image_refine.shape[1])
                    x_change = depth_image_refine.shape[1] - x
                    x_change_0 = int(np.floor(x_change/2))
                    #print('x_change_0',x_change_0)
                    round_checker = x_change/2 - x_change_0
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0

                    depth_image_refine = np.delete(depth_image_refine, np.s_[:x_change_0], 1)
                    #print('after 0 refine',depth_image_refine.shape[1])
                    depth_image_refine = np.delete(depth_image_refine, np.s_[depth_image_refine.shape[1] - x_change_max:], 1)
                    #print('after max refine', depth_image_refine.shape[1],depth_frame)

                #ここから配列入力
                depth_image_filtered = cv2.blur(depth_image_refine,ksize=(size,size))
                _,depth_image_for_input = cv2.threshold(depth_image_refine, 0.4, 255,cv2.THRESH_BINARY)
                array[:,:,depth_frame]= depth_image_for_input
            array = np.flip(np.flip(np.flip(array,2).transpose(2,0,1),0),2)
            array = np.flip(array,1)
            return array


    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #make_map_side関数ここまで

#斜め切り出し関数
def cut_rotate(img,size,deg):
    #check.show('base',img)
    center = (img.shape[1]/2, img.shape[0]/2)
    rot_mat = cv2.getRotationMatrix2D(center, deg, 1.0)
    rot_mat[0][2] += -center[0]+size[0]/2 # -(元画像内での中心位置)+(切り抜きたいサイズの中心)
    rot_mat[1][2] += -center[1]+size[1]/2 # 同上
    rotate_img = cv2.warpAffine(img, rot_mat, size)
    #check.show('rotate',rotate_img)
    return rotate_img
#ここまで斜め切り出し関数

#斜め配列の縮小
def Rotate_and_Shlink_from_side_upper(map,theta):
    theta = theta
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    #入れ子用新map作成
    map_oblique_true = Make_3D_Array(y_range,x_range,z_range)
    for slide in range(x):
        view = map[:,slide,:]
        size = (y_range,z_range)
        view_rotated = cut_rotate(view,size,theta)
        map_oblique_true[:,slide,:] = view_rotated

    return map_oblique_true

def Rotate_front(map,degree):
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    map_for_return = make_3D_array(y_range,x_range,z_range)
    for i in range(y):
        slice = map[i,:,:]
        slice_rotated=cut_rotate(slice,(slice.shape[1],slice.shape[0]),degree)
        map_for_return[i,:,:] = slice_rotated
    return map_for_return

def Rotate_side(map,degree):
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    map_for_return = make_3D_array(y_range,x_range,z_range)
    for i in range(y):
        slice = map[i,:,:]
        slice_rotated=cut_rotate(slice,(slice.shape[1],slice.shape[0]),degree)
        map_for_return[i,:,:] = slice_rotated
    return map_for_return
