import numpy as np
import cv2
import sys
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors

#撮影空間との距離を指定
dist = 100

#予定される合成空間のサイズ指定
depth = 100
#カメラのパラメータ
A = 0.0008625821
B = 0.03849
threshold = 100
#三次元配列の入力切り替え用
image_count = 0

#収納予定の三次元空間配列作成 depth×y×x
map_front = np.zeros((depth,depth,depth)).reshape(depth,depth,depth)
#print(map_front.shape[0],map_front.shape[1],map_front.shape[2])

map_side = np.zeros((depth,depth,depth)).reshape(depth,depth,depth)
#print(map_side.shape[0],map_side.shape[1],map_side.shape[2])



images = glob.glob('*.JPG')

try:
    for fname in images:
        img = cv2.imread(fname)
        image_count = image_count+1
        im_height = img.shape[0]
        im_width = img.shape[1]
        #print('im_height',im_height,'im_width',im_width)
        #print('readimage_success')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #print('grayimage_success')
        #cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
        #cv2.imshow('gray', gray)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




        for depth_frame in range(depth):
            conv = A*(dist + depth_frame) - B
            #depth_imageがそのdepthでの実サイズ配列
            depth_image_gray = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))
            ret, depth_image = cv2.threshold(depth_image_gray, threshold, 255, cv2.THRESH_BINARY)
            depth_image = depth_image/255
            #print('depth_image_y',depth_image.shape[0])
            #print('depth_image_x',depth_image.shape[1])

            #cv2.namedWindow('depth_image', cv2.WINDOW_NORMAL)
            #cv2.imshow('depth_image', depth_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            depth_image_object = np.where(depth_image == 1)
            #print(depth_image_object[1])
            #画素値が1のy座標が最大になる要素数ymax
            ymax = np.ndarray.max(depth_image_object[0])
            #print('ymax',ymax)

            #ymaxを下端として上方向に100積む
            #サイズ調整
            #足りないものは増やし、多いものは減らして100*100に持っていく
            depth_image_deleted = np.delete(depth_image, np.s_[ymax+1:], 0)
            #縦方向引き伸ばし用の行列上に積む
            refine_y_array = np.zeros((100-ymax-1, depth_image.shape[1]))
            #積む
            depth_image_refine = np.vstack((refine_y_array, depth_image_deleted))

            #横方向引き伸ばし
            #x軸方向の変化を求める(100より少ないケース)
            if depth_image_refine.shape[1] < 100:
                #print('upgrade')
                x_change = 100 - depth_image_refine.shape[1]
                x_change_0 = int(np.floor(x_change/2))
                round_checker = x_change/2 - x_change_0
                #四捨五入はroundだとバグりそうなので
                if round_checker >= 0.5:
                    x_change_max = x_change_0+1
                else:
                    x_change_max = x_change_0
                #print('x_change_0', x_change_0)
                #print('x_change_max',x_change_max)

                refine_x_0_array = np.zeros((100,x_change_0))
                refine_x_max_array = np.zeros((100, x_change_max))
                depth_image_refine = np.hstack((refine_x_0_array,depth_image_refine))
                depth_image_refine = np.hstack((depth_image_refine, refine_x_max_array))

            #x軸調整(100より多いケース)
            elif depth_image_refine.shape[1] > 100:
                #print('reduce',depth_image_refine.shape[1])
                x_change = depth_image_refine.shape[1] - 100
                x_change_0 = int(np.floor(x_change/2))
                #print('x_change_0',x_change_0)
                round_checker = x_change/2 - x_change_0
                if round_checker >= 0.5:
                    x_change_max = x_change_0+1
                else:
                    x_change_max = x_change_0
                #print('x_change_max', x_change_max)
                depth_image_refine = np.delete(depth_image_refine, np.s_[:x_change_0], 1)
                #print('after 0 refine',depth_image_refine.shape[1])
                depth_image_refine = np.delete(depth_image_refine, np.s_[depth_image_refine.shape[1] - x_change_max:], 1)
                #print('after max refine',depth_image_refine.shape[1])

            #print('depth_image_y',depth_image.shape[0])
            #print('depth_image_deleted_y',depth_image_deleted.shape[0])
            #print('depth_image_refine_y',depth_image_refine.shape[0])
            #print('depth_image_x',depth_image.shape[1])
            #print('depth_image_refine_x',depth_image_refine.shape[1])
            #cv2.namedWindow('depth_image_deleted', cv2.WINDOW_NORMAL)
            #cv2.imshow('depth_image_deleted', depth_image_deleted)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            #cv2.namedWindow('depth_image_refine', cv2.WINDOW_NORMAL)
            #cv2.imshow('depth_image_refine', depth_image_refine)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

            #3次元配列に入力
            if image_count == 1:
                map_front[depth_frame]=depth_image_refine

            else:
                map_side[depth_frame]= depth_image_refine

        #3次元配列の掛け算
        map_true = map_front * map_side.transpose(2,1,0)
        map_true = map_true.T


        x_list=[i for i in range(100)]
        y_list=[i for i in range(100)]
        z_list=[i for i in range(100)]

        fig = plt.figure()
        ax = fig.add_subplot(111,projection="3d")

        mask = map_true==1
        X,Y,Z=np.meshgrid(x_list,y_list,z_list)
        ax.set_xlabel("x",labelpad=10,fontsize=24)
        ax.set_ylabel("y",labelpad=10,fontsize=24)
        ax.set_zlabel("z",labelpad=10,fontsize=24)
        ax.set_xlim(100,0)
        ax.set_ylim(0,100)
        ax.set_zlim(0,100)
        ax.scatter(X[mask], Y[mask], Z[mask],map_true)
        plt.show()
        print('X',X[mask].ravel())
        print('Y',Y[mask].ravel())
        print('Z',Z[mask].ravel())











except:
    import sys
    print("Error:", sys.exc_info()[0])
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))
