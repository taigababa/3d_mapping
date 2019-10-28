

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
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_zlim(100,0)
    ax.scatter(X[mask],Y[mask],Z[mask],map,c='cyan',alpha=0.01)
    mask2 = map==2
    ax.scatter(X[mask2],Y[mask2],Z[mask2],map,c='pink')

    plt.show()

def Show_3D_3COLOR(map):
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
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    ax.set_zlim(100,0)
    ax.scatter(X[mask],Y[mask],Z[mask],map,c='cyan',alpha=0.01)
    mask2 = map==2
    ax.scatter(X[mask2],Y[mask2],Z[mask2],map,c='lime',alpha=0.1)
    mask3 = map==3
    ax.scatter(X[mask3],Y[mask3],Z[mask3],map,c='pink')

    plt.show()
