import numpy as np
import cv2
import sys
import glob

try:
    img = cv2.imread("Lenna.png")

    if img is None:
        print("ファイルを開けません")
        import sys
        sys.exit()

    SCALE1 = 0.5
    SCALE2 = 1.62

    height = img.shape[0]
    width = img.shape[1]

    dst = cv2.resize(img, (int(width*SCALE1), int(width*SCALE2)))
    cv2.imwrite('resize_Lenna.jpg', dst)
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(gray, 100, 200, cv2.THRESH_BINARY)
    print(dst/200)
    cv2.namedWindow('dst', cv2.WINDOW_NORMAL)
    cv2.imshow('dst', dst)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

except:
    import sys
    print("Error:", sys.exc_info(0))
    print(sys.exc_info()[1])
    import traceback
    print(traceback.format_tb(sys.exc_info()[2]))
