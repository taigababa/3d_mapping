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

#撮影空間との距離を想定[mm]
dist = 100

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

#3次元配列作成関数
def Make_3D_Array(y,x,z):
    #array上での次元と座標系ではx,yが入れ替わる
    array_3D = np.zeros((y,x,z)).reshape(y,x,z)

    return array_3D



#3次元配列入力関数
def Fill_3D_Array(filename,array,threshold,dist):
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

            """
            #ここからチンアナゴ抽出
            #本来は識別機を用いてやるが，今回はthresholdでごまかす
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            gray = gray/255
            #check.show('gray',gray)
            #一応確認用
            #cv2.imshow('gray',gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            """
            #BGRをHSVに変換
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h_img, s_img, v_img = cv2.split(hsv)
            _, gray = cv2.threshold(v_img, threshold, 255,cv2.THRESH_BINARY )
            gray = gray/255
            #ここからz軸に対してスライス(xy平面)ごとに入力
            for depth_frame in range(z):
                #変形倍率convの計算
                conv = (A*(dist + depth_frame) - B)/3
                #depth_image_grayはそのdepthでの実サイズ画像
                depth_image = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))

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
                array[:,:,depth_frame]= depth_image_refine
                #check.show('slice',depth_image_refine)

                #print('x_low:',array[:,:,depth_frame].shape[1],' y_low:',array[:,:,depth_frame].shape[0])



    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #fill関数ここまで

def Fill_3D_Array_REV(filename,array,threshold,dist):
    print('rev')
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

            """
            #ここからチンアナゴ抽出
            #本来は識別機を用いてやるが，今回はthresholdでごまかす
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            gray = gray/255
            #check.show('gray',gray)
            #一応確認用
            #cv2.imshow('gray',gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            """
            #BGRをHSVに変換
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h_img, s_img, v_img = cv2.split(hsv)
            _, gray = cv2.threshold(v_img, threshold, 255,cv2.THRESH_BINARY )
            gray = gray/255
            #ここからz軸に対してスライス(xy平面)ごとに入力
            for depth_frame in range(z):
                #変形倍率convの計算
                conv = (A*(dist + depth_frame) - B)/3
                #depth_image_grayはそのdepthでの実サイズ画像
                depth_image = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))

                #ここからサイズ調節
                ysize = depth_image.shape[0]


                #縦方向引き伸ばし
                if ysize <= y:
                    print('y_upgrade')
                    y_change = y - ysize
                    y_change_0 = int(np.floor(y_change/2))
                    round_checker_y = y_change/2 - y_change_0
                    #roundではやばそうなので丁寧の処理
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0

                    print(y_change_0,y_change_max)
                    refine_y_0_array = np.zeros((y_change_0, depth_image.shape[1]))

                    refine_y_max_array = np.zeros((y_change_max, depth_image.shape[1]))


                    depth_image_refine = np.vstack((refine_y_0_array,depth_image))
                    depth_image_refine = np.vstack((depth_image_refine, refine_y_max_array))
                    print('add y refine',depth_image_refine.shape[0],depth_frame)

                #縦方向削るパターン
                elif ysize > y:
                    print('reduce',depth_image.shape[0])
                    y_change = ysize - y
                    #floorは切り捨て
                    y_change_0 = int(np.floor(y_change/2))
                    print('y_change',y_change)
                    print('y_change_0',y_change_0)
                    round_checker_y = y_change/2 - y_change_0
                    if round_checker_y >= 0.5:
                        y_change_max = y_change_0+1
                    else:
                        y_change_max = y_change_0
                    print('y_change_max',y_change_max)
                    depth_image_refine_0 = np.delete(depth_image, np.s_[:y_change_0], 0)
                    print('after 0 refine',depth_image_refine_0.shape[0])
                    depth_image_refine = np.delete(depth_image_refine_0, np.s_[depth_image_refine_0.shape[0] - y_change_max:], 0)
                    print('after max refine',depth_image_refine.shape[0])

                #横方向変化
                #横方向引き伸ばし
                #x軸方向の変化を求める(100より少ないケース)
                if depth_image_refine.shape[1] <= x:
                    print('upgrade')
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
                array[:,:,z - depth_frame-1]= depth_image_refine
                #check.show('slice_rev',depth_image_refine)

                #print('x_low:',array[:,:,depth_frame].shape[1],' y_low:',array[:,:,depth_frame].shape[0])



    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))

def Show_3D(map):
    x = map.shape[0]
    y = map.shape[1]
    z = map.shape[2]
    x_list =[i for i in range(x)]
    y_list =[i for i in range(y)]
    z_list =[i for i in range(z)]

    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")

    mask = map==1
    X,Y,Z=np.meshgrid(x_list,y_list,z_list)
    ax.set_xlabel("x",labelpad=10,fontsize=24)
    ax.set_ylabel("y",labelpad=10,fontsize=24)
    ax.set_zlabel("z",labelpad=10,fontsize=24)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(z,0)
    ax.scatter(X[mask],Y[mask],Z[mask],map,c='pink')
    plt.show()
#show関数ここまで

#斜め切り出し関数
def cut_rotate(img,size,deg):
    #check.show('base',img)
    center = (img.shape[0]/2, img.shape[1]/2)
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

#imgバージョン
def Fill_3D_Array_img(img,array,threshold,dist):
    x = array.shape[1]
    y = array.shape[0]
    z = array.shape[2]
    try:
        img = cv2.imread(fname)
        #元画像のx取得
        im_height = img.shape[0]
        im_width = img.shape[1]

        """
        #ここからチンアナゴ抽出
        #本来は識別機を用いてやるが，今回はthresholdでごまかす
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        gray = gray/255
        #check.show('gray',gray)
        #一応確認用
        #cv2.imshow('gray',gray)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        """
        #BGRをHSVに変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_img, s_img, v_img = cv2.split(hsv)
        _, gray = cv2.threshold(v_img, threshold, 255,cv2.THRESH_BINARY )
        gray = gray/255
        #ここからz軸に対してスライス(xy平面)ごとに入力
        for depth_frame in range(z):
            #変形倍率convの計算
            conv = (A*(dist + depth_frame) - B)/3
            #depth_image_grayはそのdepthでの実サイズ画像
            depth_image = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))

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
            array[:,:,depth_frame]= depth_image_refine
            #check.show('slice',depth_image_refine)

            #print('x_low:',array[:,:,depth_frame].shape[1],' y_low:',array[:,:,depth_frame].shape[0])




    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #fill関数ここまで
