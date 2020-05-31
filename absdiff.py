#This is a good algo but the problem is that we need a static background
#To counter this i introduced an option to reset the background by pressing 'r'
#Still human effort is needed so this is not a complete solution

import cv2
import numpy as np

vid = cv2.VideoCapture(0)
_ , background = vid.read()
background = cv2.flip(background , 1)
background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5),np.uint8)

while(True):
    ret , frame = vid.read()
    if not ret:
        print("Frames not read correctly")
        break
    else:
        frame = cv2.flip(frame , 1)
        frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

    fg = cv2.absdiff(frame , background)
    closing = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel)
    _, thresholded = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imshow("original" , frame)
    cv2.imshow("absdiff" , fg)
    cv2.imshow("thresholded" , thresholded)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
    elif cv2.waitKey(1) & 0xff == ord('r'):
        _ , background = vid.read()
        background = cv2.flip(background , 1)
        background = cv2.cvtColor(background , cv2.COLOR_BGR2GRAY)


cv2.destroyAllWindows()