#This is not providing good results

import cv2
import numpy as np

vid = cv2.VideoCapture(0)
fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while(True):
    ret , frame = vid.read()
    if not ret:
        print("Frames not read correctly")
        break
    else:
        frame = cv2.flip(frame , 1)

    fg = fgbg.apply(frame)
    cv2.imshow("original" , frame)
    cv2.imshow("MOG1" , fg)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()