import numpy as np
import cv2
import sys
import glob

#撮影空間との距離を指定
dist = 100

#予定される合成空間のサイズ指定
depth = 1

#カメラのパラメータ
A = 0.0008625821
B = 0.03849
threshold = 100
#三次元配列の入力切り替え用
image_count = 0

#収納予定の三次元空間配列作成
map_front = np.zeros((depth,depth,depth))
print(map_front.shape[0],map_front.shape[1],map_front.shape[2])

map_side = np.zeros((depth,depth,depth))
print(map_side.shape[0],map_side.shape[1],map_side.shape[2])



images = glob.glob('*.JPG')

try:
    for fname in images:
        img = cv2.imread(fname)
        image_count = image_count+1
        im_height = img.shape[0]
        im_width = img.shape[1]
        print('im_height',im_height,'im_width',im_width)
        print('readimage_success')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print('grayimage_success')
        cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
        cv2.imshow('gray', gray)

        cv2.waitKey(0)
        cv2.destroyAllWindows()




        for depth_frame in range(depth):
            conv = A*(dist + depth_frame) - B
            #depth_imageがそのdepthでの実サイズ配列
            depth_image_gray = cv2.resize(gray, (int(im_width*conv), int(im_height*conv)))
            ret, depth_image = cv2.threshold(depth_image_gray, threshold, 255, cv2.THRESH_BINARY)
            depth_image = depth_image/255
            print('depth_image_y',depth_image.shape[0])
            print('depth_image_x',depth_image.shape[1])

            cv2.namedWindow('depth_image', cv2.WINDOW_NORMAL)
            cv2.imshow('depth_image', depth_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            depth_image_object = np.where(depth_image == 1)
            #print(depth_image_object[1])
            #画素値が1のy座標が最大になる要素数ymax
            ymax = np.ndarray.max(depth_image_object[0])
            print('ymax',ymax)

            #ymaxを下端として上方向に100積む
            #サイズ調整
            #足りないものは増やし、多いものは減らして100*100に持っていく
            depth_image_deleted = np.delete(depth_image, np.s_[ymax+1:], 0)
            #縦方向引き伸ばし用の行列上に積む
            refine_y_array = np.zeros((100-ymax-1, depth_image.shape[1]))
            #積む
            depth_image_refine = np.vstack((refine_y_array, depth_image_deleted))

            #横方向引き伸ばし

            print('depth_image',depth_image.shape[0])
            print('depth_image_deleted',depth_image_deleted.shape[0])
            print('depth_image_refine',depth_image_refine.shape[0])
            cv2.namedWindow('depth_image_deleted', cv2.WINDOW_NORMAL)
            cv2.imshow('depth_image_deleted', depth_image_deleted)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            cv2.namedWindow('depth_image_refine', cv2.WINDOW_NORMAL)
            cv2.imshow('depth_image_refine', depth_image_refine)
            cv2.waitKey(0)
            cv2.destroyAllWindows()





            #3次元配列に入力
            #if image_count == 1:
                #map_frontに代入
            #else:
                #map_sideに代入


except:
    import sys
    print("Error:", sys.exc_info()[0])
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))
