#計算用モジュール
import numpy as np

#画像処理モジュール
import cv2
import math

import sys
#ファイルのパス名を利用するモジュール
import glob

import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as colors
import Hireso_projection as Hi_PROJECTION



x_list =[i for i in range(100)]
y_list =[i for i in range(100)]
z_list =[i for i in range(100)]

fig = plt.figure()
ax = fig.add_subplot(111,projection="3d")

map = Hi_PROJECTION.make_3D_array(100,100,100)
mask = map==1
Y,X,Z=np.meshgrid(y_list,x_list,z_list)

#ax.plot_surface(Y,X,Z)
print(X)
ax.scatter(Y[mask],X[mask],Z[mask],map,c="black",alpha=1)


for i in range(11):
    #上面y=100固定
    plt.plot([i*10,i*10],[100,100],[0,100],color = "black")
    plt.plot([0,100],[100,100],[i*10,i*10],color = "black")

    #正面z=0固定
    plt.plot([i*10,i*10],[0,100],[0,0],color = "black")
    plt.plot([0,100],[i*10,i*10],[0,0],color = "black")

    #右x=100固定
    plt.plot([100,100],[0,100],[i*10,i*10], color = "black")
    plt.plot([100,100],[i*10,i*10],[0,100], color = "black")

ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

plt.show()
