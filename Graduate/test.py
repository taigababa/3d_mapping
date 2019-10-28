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

#自作モジュール
import check as CHECK
import Projection as PROJECTION
import demo_extractor as DEMO

"""
images = glob.glob('*.JPG')
for fname in images:
    DEMO.thresh_checker(fname)
"""
DEMO.thresh_checker('IMG_8810.JPG')
a_3d = np.arange(24).reshape(2, 3, 4)
a_3d = a_3d.transpose(1,0,2)
print(a_3d.shape)
