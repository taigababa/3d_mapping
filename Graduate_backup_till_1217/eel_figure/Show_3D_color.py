

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
from mayavi import mlab


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
    Y,X,Z=np.meshgrid(y_list,x_list,z_list)
    mask = map==1
    ax.set_xlabel("x",labelpad=10,fontsize=24)
    ax.set_ylabel("y",labelpad=10,fontsize=24)
    ax.set_zlabel("z",labelpad=10,fontsize=24)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(0,z)
    ax.scatter(Y[mask],X[mask],Z[mask],map,c=color,alpha=alpha,s=30)
    plt.show()

def show_3D_color_3colors(map1,color1,alpha1,map2,color2,alpha2,map3,color3,alpha3,map4,color4,alpha4):
    x = map1.shape[1]
    y = map1.shape[0]
    z = map1.shape[2]
    x_list =[i for i in range(x)]
    y_list =[i for i in range(y)]
    z_list =[i for i in range(z)]

    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")
    Y,X,Z=np.meshgrid(y_list,x_list,z_list)
    mask1 = map1==1
    mask2 = map2==1
    mask3 = map3==1
    mask4 = map4==1
    ax.set_xlabel("x",labelpad=10,fontsize=24)
    ax.set_ylabel("y",labelpad=10,fontsize=24)
    ax.set_zlabel("z",labelpad=10,fontsize=24)
    ax.set_xlim(0,x)
    ax.set_ylim(0,y)
    ax.set_zlim(0,z)
    ax.scatter(Y[mask1],X[mask1],Z[mask1],map1,c=color1,alpha=alpha1,s=30)
    ax.scatter(Y[mask2],X[mask2],Z[mask2],map2,c=color2,alpha=alpha2,s=30)
    ax.scatter(Y[mask3],X[mask3],Z[mask3],map3,c=color3,alpha=alpha3,s=30)
    ax.scatter(Y[mask4],X[mask4],Z[mask4],map4,c=color4,alpha=alpha4,s=30)
    plt.show()
