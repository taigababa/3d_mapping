import cv2
import numpy as np
import math
import glob
import sys

#自作パッケージ

import check
import Show_3D_add as ADD
import Show_3D_color as COLOR

thresh = 0
thresholdType = cv2.THRESH_BINARY_INV
max_val = 255

def changethresh(pos):
    global thresh
    thresh = pos



def thresh_checker(fname,mode):
    img = cv2.imread(fname)
    #BGRをHSVに変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #HSVに分解
    h_img, s_img, v_img = cv2.split(hsv)
    #r_img,g_img,b_img = cv2.split(img)
    #ウィンドウの名前を設定
    cv2.namedWindow("img",cv2.WINDOW_NORMAL)
    cv2.namedWindow("thresh",cv2.WINDOW_NORMAL)
    #トラックバーのコールバック関数の設定
    cv2.createTrackbar("trackbar", "thresh", 0, 255, changethresh)
    while(1):

        cv2.imshow("img", img)
        if(mode==1):
            _, thresh_img = cv2.threshold(h_img, thresh, max_val, thresholdType)
        elif(mode == 2):
            _, thresh_img = cv2.threshold(s_img, thresh, max_val, thresholdType)
        else:
            _, thresh_img = cv2.threshold(v_img, thresh, max_val, thresholdType)

        cv2.imshow("thresh", thresh_img)
        k = cv2.waitKey(1)
        #Escキーを押すと終了
        if k == 27:
            print('no save')
            break
        #sを押すと結果を保存
        if k == ord("s"):
            #result = cv2.merge(cv2.split(img) + [thresh_img])
            result = thresh_img
            cv2.imwrite(fname[:fname.rfind(".")] + "_result.png", result)
            print('saved')
            break


"""
    check.show('h',hsv[:,:,0])
    check.show('s',hsv[:,:,1])
    check.show('v',hsv[:,:,2])
"""
