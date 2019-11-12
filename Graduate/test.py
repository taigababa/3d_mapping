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

print('filename?')
str = input()
print('mode?(h=0,s=1,v=2)')
mode = input()
DEMO.thresh_checker(str,mode)
