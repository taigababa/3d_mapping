import cv2
import numpy as np
import math

#自作パッケージ
import slope_3D_mapping as slope
import check
import Show_3D_add as ADD
import Show_3D_color as COLOR

x_range = 100
y_range = 100
z_range = 100
threshold = 150
theta = 30
size = (100,100)
sin = math.sin(math.radians(theta))
cos = math.cos(math.radians(theta))

x_range_oblique = (int)(x_range*sin + z_range*cos)
y_range_oblique = y_range
z_range_oblique = (int)(x_range*cos + z_range*sin)

map_front = slope.Make_3D_Array(y_range,x_range,z_range)
slope.Fill_3D_Array('IMG_5674.JPG',map_front)

map_side = slope.Make_3D_Array(y_range,x_range,z_range)
slope.Fill_3D_Array('IMG_5675.JPG',map_side)

map_oblique = slope.Make_3D_Array(y_range_oblique,x_range_oblique,z_range_oblique)
slope.Fill_3D_Array('IMG_7885.JPG',map_oblique)
map_oblique_true = slope.Rotate_and_Shlink_from_side_upper(map_oblique,theta)

map_add = map_front + map_side.transpose(0,2,1)
map_true = map_front * map_side.transpose(0,2,1)
ADD.Show_3D(map_add.transpose(2,1,0))
slope.Show_3D(map_true.transpose(2,1,0))
COLOR.Show_3D_color(map_front.transpose(2,1,0),'cyan',1)
COLOR.Show_3D_color(map_side.transpose(0,2,1).transpose(2,1,0),'cyan',1)
COLOR.Show_3D_color(map_true,'cyan',0)
