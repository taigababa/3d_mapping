import numpy as np
import cv2
import sys
import glob
distance = '300mm'
path_w = 'olympus_distance_300mm.csv'

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

images = glob.glob('*.JPG')


imgpoints = []
objpoints = []
dist = []


try:
    for fname in images:
        img = cv2.imread(fname)
        print('readimage_success')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print('grayimage_success')



        ret, corners = cv2.findChessboardCorners(gray, (7,6),None)


        if ret == True:

            print('getcorner success')
            print(fname)
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)



            corners2_shift_width = np.roll(corners2,2)
            #一つ前の座標セットとの差が取れる
            corners2_diff_width = corners2 - corners2_shift_width
            #print(corners2_diff_width)

            #配列を0-41から36-41,0-35に並び替える
            corners2_shift_height = np.roll(corners2, 14)
            #7個あととの比較
            corners2_diff_height = corners2 - corners2_shift_height
            #corners2_diff_height[6+7の倍数]をみれば縦の変位がみられる
            print(corners2_diff_height)


            #corners_diff[1]で1つめと2つめの座標の配列さらに[1][0,1]でy座標のみとりだせる

            #7の倍数番目は上下段の差を取っているのでいらない
            for num in range(42):
                if not num % 7:
                    continue
                else:
                    dist.append(np.sqrt(np.square(corners2_diff_width[num]).sum(axis=1)))

            for num in range(35):
                num += 7
                dist.append(np.sqrt(np.square(corners2_diff_height[num]).sum(axis=1)))
                #print(corners2_diff_height[6+7*num][0,1]/6)




            img = cv2.drawChessboardCorners(img, (7,6),corners2,ret)
            cv2.namedWindow(fname, cv2.WINDOW_NORMAL)
            cv2.imshow(fname,img)
            cv2.waitKey(0)

            #ここからファイル出力
            np.savetxt(path_w, dist, delimiter=',')

        else:
            print('failed')







except:
    print("ERROR:",sys.exc_info()[0])
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))
