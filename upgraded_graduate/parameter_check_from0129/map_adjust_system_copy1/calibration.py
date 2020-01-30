#
# カメラの歪みを戻すための値を計算する
#
import numpy as np
import cv2
import glob
from time import sleep
from datetime import datetime
import os


MTX_PATH ="mtx.csv"
DIST_PATH ="dist.csv"

# メイン関数
def main():
    calcCamera() # カメラの歪みを計算

# カメラの歪みを計算する関数
def calcCamera():
    square_size = 20.0      # 正方形のサイズ(mm)
    pattern_size = (8, 8)  # 模様のサイズ
    pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    for fn in glob.glob("./img/*"):
        # 画像の取得
        im = cv2.imread(fn,0)
        print ("loading..." + fn)
        # チェスボードのコーナーを検出
        found, corners = cv2.findChessboardCorners(im,pattern_size,None)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(im, corners, (11,11), (-1,-1), term)
            # マークをつけて画像保存
            img = cv2.drawChessboardCorners(im, pattern_size, corners2, found)
            saveImgByTime(img)
            sleep(1)
        # コーナーがない場合のエラー処理
        if not found:
            print ('chessboard not found')
            continue
        img_points.append(corners.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        obj_points.append(pattern_points)

    # 内部パラメータを計算
    rms, K, d, r, t = cv2.calibrateCamera(obj_points, img_points, (im.shape[1],im.shape[0]), None, None)

    # 計算結果を表示
    print ("RMS = ", rms)
    print ("K = \n", K)
    print ("d = ", d.ravel())

    # ファイル保存
    os.chdir("./temp")
    saveCalibrationFile(K, d, MTX_PATH, DIST_PATH)
    os.chdir("../")

# キャリブレーションCSVファイルを上書き保存する関数
def saveCalibrationFile(mtx, dist, mtx_path, dist_path):
    np.savetxt(mtx_path, mtx, delimiter =',',fmt="%0.14f")   #カメラ行列の保存
    np.savetxt(dist_path, dist, delimiter =',',fmt="%0.14f") #歪み係数の保存

# 画像を時刻で保存する関数
def saveImgByTime(img):
    os.chdir("./temp")
    # 時刻を取得
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = date + ".png"
    cv2.imwrite(path, img) # ファイル保存
    print("saved: ", path)
    os.chdir("../")
if __name__ == '__main__':
    main()
