import cv2
import numpy as np
import math
import glob
import sys

#自作パッケージ
import check
import Show_3D_add as ADD
import Show_3D_color as COLOR
import Projection as PROJECTION
import demo_extractor as DEMO

x_range = 100
y_range = 100
z_range = 100
threshold = 240
theta = math.degrees(math.atan2(8,10))

size = (100,100)
sin = math.sin(math.radians(theta))
cos = math.cos(math.radians(theta))

x_range_oblique = x_range
y_range_oblique = (int)(y_range*sin + z_range*cos)
z_range_oblique = (int)(y_range*cos + z_range*sin)


map_front = PROJECTION.Make_3D_Array(y_range,x_range,z_range)
PROJECTION.Fill_3D_Array('IMG_8775.JPG',map_front,248,100)


map_side = PROJECTION.Make_3D_Array(y_range,x_range,z_range)
PROJECTION.Fill_3D_Array('IMG_8776.JPG',map_side,235,100)
map_side = map_side.transpose(0,2,1)


map_oblipue = PROJECTION.Make_3D_Array(y_range_oblique,x_range_oblique,z_range_oblique)
PROJECTION.Fill_3D_Array('IMG_8777.JPG',map_oblipue,245,128)
map_oblique_true = PROJECTION.Rotate_and_Shlink_from_side_upper(map_oblipue,theta)


slice = map_oblique_true[:,:,z_range-1]
map_nest = PROJECTION.Make_3D_Array(y_range,x_range,z_range)
PROJECTION.Fill_3D_Array_img(slice,map_nest,threshold,128)

map_true = map_front * map_side * map_oblique_true
map_add = map_front + map_side + map_oblique_true


#COLOR.Show_3D_color(map_oblique_true,'cyan',1)
#COLOR.Show_3D_color(map_front,'cyan',1)
#COLOR.Show_3D_color(map_side,'cyan',1)
COLOR.Show_3D_color(map_true,'cyan',1)
#ADD.Show_3D(map_add.transpose(1,0,2))
#ADD.Show_3D_3COLOR(map_add.transpose(1,0,2))
#COLOR.Show_3D_color(map_oblipue,'cyan',1)
COLOR.Show_3D_color(map_oblique_true,'cyan',1)
slice = map_oblique_true[:,:,z_range-1]
#check.show('slice',slice)
#cv2.imwrite('nest.JPG',slice)

"""
img = cv2.imread('IMG_8777.JPG')
size = (img.shape[0],img.shape[1])
PROJECTION.cut_rotate(img,size,theta)
"""
#DEMO.thresh_checker('IMG_8776.JPG')
