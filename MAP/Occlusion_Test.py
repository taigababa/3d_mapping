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
theta = 30
size = (100,100)
sin = math.sin(math.radians(theta))
cos = math.cos(math.radians(theta))

x_range_oblique = (int)(x_range*sin + z_range*cos)
y_range_oblique = y_range
z_range_oblique = (int)(x_range*cos + z_range*sin)

map_front = PROJECTION.Make_3D_Array(y_range,x_range,z_range)
PROJECTION.Fill_3D_Array('IMG_8775.JPG',map_front,threshold)

map_side = PROJECTION.Make_3D_Array(y_range,x_range,z_range)
PROJECTION.Fill_3D_Array('IMG_8776.JPG',map_side,235)
map_side = map_side.transpose(0,2,1)

map_oblipue = PROJECTION.Make_3D_Array(y_range_oblique,x_range_oblique,z_range_oblique)
PROJECTION.Fill_3D_Array('IMG_8777.JPG',map_oblipue,threshold)
map_oblique_true = PROJECTION.Rotate_and_Shlink_from_side_upper(map_oblipue,theta)


map_true = map_front * map_side
map_add = map_front + map_side
#COLOR.Show_3D_color(map_oblique_true,'cyan',1)
#COLOR.Show_3D_color(map_front,'cyan',1)
#COLOR.Show_3D_color(map_side,'cyan',1)
COLOR.Show_3D_color(map_true,'cyan',1)
ADD.Show_3D(map_add.transpose(2,1,0))

#DEMO.thresh_checker('IMG_8779.JPG')
