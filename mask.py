import cv2
import numpy as np
import mouse

vid = cv2.VideoCapture(0)
lower_red = np.array([165, 120, 100])
upper_red = np.array([179, 255, 255])
mouse.move(100, 100, absolute=True, duration=0.2)
while True:
    cnt = []
    co_ordinate = []
    _ , frame = vid.read()

    frame = cv2.flip(frame , 1)
    mask = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(mask , lower_red , upper_red)
    result = cv2.bitwise_and(frame , frame , mask = mask)
    image, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE )
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000 and area < 3000:
            cnt.append(i)
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            co_ordinate.append((cx , cy))
            print(area)
    img = cv2.drawContours(mask, cnt, -1, (0,0,255), 3)
    for i in co_ordinate:
        frame = cv2.circle(frame,i, 5, (0,0,255), -1)

    cv2.imshow("frame" , frame)
    cv2.imshow("Mask" , mask)
    cv2.imshow("result" , result)
    cv2.imshow("img" , img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cv2.destroyAllWindows()
