#ここに斜めありver.の視体積交差アルゴリズムを書いていく

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

#撮影空間との距離を想定[mm]
dist = 100

#合成空間のサイズを指定
x_range = 100
y_range = 100
z_range = 100

#カメラのパラメータ
#y = ax + bの形
A = 0.0008625821
B = 0.03849

#threshold用
threshold = 100

#3次元配列作成関数
def Make_3D_Array(x,y,z):
    array_3D = np.zeros((x,y,z)).reshape(x,y,z)
    return array_3D


#3次元配列入力関数
def Fill_3D_Array(filename,x,y,z,array):
    images = glob.glob(filename)
    try:
        for fname in images:
            img = cv2.imread(fname)
            #元画像のx取得
            im_height = img.shape[0]
            im_width = img.shape[1]

            #ここからチンアナゴ抽出
            #本来は識別機を用いてやるが，今回はthresholdでごまかす
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, gray = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            gray = gray/255
            #一応確認用
            #cv2.imshow('gray',gray)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            #ここからz軸に対してスライス(xy平面)ごとに入力
            for depth_frame in range(z):
                #変形倍率convの計算
                conv = A*(dist + depth_frame) - B
                #depth_image_grayはそのdepthでの実サイズ画像
                depth_image = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))

                #ここからサイズ調節
                #画素値が1(チンアナゴ)の座標をdepth_image_objectに代入
                depth_image_object = np.where(depth_image == 1)
                #画素値が1のy座標の最大値,つまり画像的には下限(地面)を求める
                ymax = np.ndarray.max(depth_image_object[0])
                #ymaxを下端として不要部分を削除
                depth_image_deleted = np.delete(depth_image, np.s_[ymax+1:],0)
                #ymaxより下の部分に合成するようの行列を作成
                refine_y_array = np.zeros(((y- ymax-1), depth_image.shape[1]))
                #積む
                depth_image_refine = np.vstack((refine_y_array, depth_image_deleted))


                #横方向引き伸ばし
                #x軸方向の変化を求める(100より少ないケース)
                if depth_image_refine.shape[1] < x:
                    #print('upgrade')
                    x_change = x - depth_image_refine.shape[1]
                    x_change_0 = int(np.floor(x_change/2))
                    round_checker = x_change/2 - x_change_0
                    #四捨五入はroundだとバグりそうなので
                    if round_checker >= 0.5:
                        x_change_max = x_change_0+1
                    else:
                        x_change_max = x_change_0


                    refine_x_0_array = np.zeros((x,x_change_0))

                    refine_x_max_array = np.zeros((x, x_change_max))

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
                    #print('after max refine', depth_image_refine.shape[1])


                #ここから配列入力
                array[depth_frame]= depth_image_refine



    except:
            import sys
            print("Error:", sys.exc_info()[0])
            print(sys.exc_info()[1])
            import traceback
            print(traceback.format_tb(sys.exc_info()[2]))
            #fill関数ここまで

def Show_3D(x,y,z,map):
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
    ax.set_xlim(100,0)
    ax.set_ylim(0,100)
    ax.set_zlim(0,100)
    ax.scatter(X[mask],Y[mask],Z[mask],map)
    plt.show()
#show関数ここまで



#正面方向作成
map_front = Make_3D_Array(x_range,y_range,z_range)
Fill_3D_Array('IMG_5674.JPG',x_range,y_range,z_range,map_front)

#横方向作成
map_side = Make_3D_Array(x_range,y_range,z_range)
Fill_3D_Array('IMG_5675.JPG',x_range,y_range,z_range,map_side)

map_true = map_front*map_side.transpose(2,1,0)
map_true = map_true.T

Show_3D(x_range,y_range,z_range,map_true)
