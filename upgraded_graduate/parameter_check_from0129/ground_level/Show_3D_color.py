

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
import matplotlib.cm as cm

#計算用
import math

def show_3D_color(map,color,alpha):
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    x_list =[i for i in range(x)]
    y_list =[i for i in range(y)]
    z_list =[i for i in range(z)]

    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")

    mask = map==1
    Y,X,Z=np.meshgrid(y_list,x_list,z_list)
    ax.set_xlabel("x",labelpad=10,fontsize=24)
    ax.set_ylabel("y",labelpad=10,fontsize=24)
    ax.set_zlabel("z",labelpad=10,fontsize=24)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(0,z)
    ax.scatter(Y[mask],X[mask],Z[mask],map,c=color,alpha=alpha)


    plt.show()

def show_3D_color_nolabel(map,color,alpha):
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    x_list =[i for i in range(x)]
    y_list =[i for i in range(y)]
    z_list =[i for i in range(z)]

    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")

    mask = map==1
    Y,X,Z=np.meshgrid(y_list,x_list,z_list)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(0,z)
    ax.scatter(Y[mask],X[mask],Z[mask],map,c=color,alpha=alpha)
    #plt.tick_params(length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


    plt.show()

def show_heat_color_nolabel(map,color,alpha):
    x = map.shape[1]
    y = map.shape[0]
    z = map.shape[2]
    x_list =[i for i in range(x)]
    y_list =[i for i in range(y)]
    z_list =[i for i in range(z)]

    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")

    mask = map==1
    Y,X,Z=np.meshgrid(y_list,x_list,z_list)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(0,z)
    ax.scatter(Y[mask],X[mask],Z[mask],map,c=cm.jet((X[mask]-50)/5),alpha=alpha)

    #plt.tick_params(length=0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


    plt.show()
