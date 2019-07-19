import numpy as np
import math

im_dist = 100
dist = 300
depth = 5
#ここには2値化した画像を入力
#ここではダミーで対応
front_view = np.zeros((300,400))
for x in range(3):
    for y in range(3):
        front_view[150+x][200+y]=1


#obj_index[x=0,y=1][番目]で情報を取り出せる
obj_index = list(np.where(front_view==1))

#中心からの距離に変換
#各要素のX座標を中心からの距離に変換
obj_index[0]-=math.ceil(front_view.shape[0] / 2)
#各要素のY座標を中心からの距離に変換
obj_index[1]-=math.ceil(front_view.shape[1] / 2)

#有色画素数の算出
obj_num = obj_index[0].size

#ボクセル空間の構築
#最奥部でのX,Yサイズの決定
#最大倍率の決定
sizemag_max = (depth+im_dist+dist)/(im_dist+dist)
#初期値でのX,Y座標の算出
x_size = front_view.shape[0]
y_size = front_view.shape[1]
final_x_size = math.ceil(x_size * sizemag_max)
final_y_size = math.ceil(y_size * sizemag_max)
projection_voxels = numpy.zeros((depth, final_x_size, final_y_size))


#ここから3次元空間合成
for depth_i in range(depth):
    #各階層での倍率を計算
    sizemag = (depth_i+im_dist+dist)/(im_dist+dist)
    for i in obj_num:
        #各有効画素の左端の座標を決定
        obj_index[0][i]*sizemag
