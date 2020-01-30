#
# カメラの歪みを補正する
#
import numpy as np
import cv2
import glob
from time import sleep
from datetime import datetime
import os


MTX_PATH = "mtx.csv"
DIST_PATH = "dist.csv"


# メイン関数
def main():
    calibrateImage() # 画像の歪みを補正

# カメラの歪みをCSVファイルを元に補正する関数
def calibrateImage():
    mtx, dist = loadCalibrationFile(MTX_PATH, DIST_PATH)

    for fn in glob.glob("./input/*"):
        img = cv2.imread(fn)
        resultImg = cv2.undistort(img, mtx, dist, None) # 内部パラメータを元に画像補正
        saveresultByTime(resultImg)
        sleep(1)

# キャリブレーションCSVファイルを読み込む関数
def loadCalibrationFile(mtx_path, dist_path):
    try:
        os.chdir("./temp")
        mtx = np.loadtxt(mtx_path, delimiter=',')
        dist = np.loadtxt(dist_path, delimiter=',')
        os.chdir("../")
    except Exception as e:
        raise e
    return mtx, dist

# 画像を時刻で保存する関数
def saveresultByTime(img):
    os.chdir("./output")
    # 時刻を取得
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = date + ".png"
    cv2.imwrite(path, img) # ファイル保存
    print("saved: ", path)
    os.chdir("../")

if __name__ == '__main__':
    main()
