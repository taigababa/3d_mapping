import numpy as np

alpha = 100
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
obj_index[0]-=150
#各要素のY座標を中心からの距離に変換
obj_index[1]-=200

for n in range(9):
    for i in range(2):
        print(obj_index[i][n])



#ここから3次元空間合成
for depth in range(5):
    sizemag = (depth+alpha)/alpha
    x_size = front_view.shape[0]
    y_size = front_view.shape[1]
    modified_x_size = int(x_size * sizemag)
    modified_y_size = int(y_size * sizemag)
    #print(modified_x_size, modified_y_size)
