import cv2
import math
import numpy as np
import mouse
import pyautogui

def dist():
    if (len(co_ordinate_for_green) and len(co_ordinate_for_blue)) == 0 :
        return 1000
    else: 
        return math.sqrt(math.pow((co_ordinate_for_green[0][1]- co_ordinate_for_blue[0][1]) , 2 ) + math.pow((co_ordinate_for_green[0][0]- co_ordinate_for_blue[0][0]) , 2 ))


def find_contours():
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE )
    return contours , hierarchy

def draw_contours(contours , frame , color):
    for i in contours:
        area = cv2.contourArea(i)
        if area > 1000 and area < 3000:
            cnt.append(i)
            M = cv2.moments(i)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if color== 'red':
                co_ordinate_for_mouse.append((cx , cy))
            elif (color == 'green'):
                co_ordinate_for_green.append((cx , cy))
            elif (color == 'blue'):
                co_ordinate_for_blue.append((cx , cy))
    img = cv2.drawContours(mask, cnt, -1, (0,0,255), 3)
    if color == 'red':
        for i in co_ordinate_for_mouse:
            frame = cv2.circle(frame,i, 5, (0,0,255), -1)
    elif (color == 'green'):
        for i in co_ordinate_for_green:
            frame = cv2.circle(frame,i, 5, (0,255,0), -1)
    elif (color == 'blue' ):
        for i in co_ordinate_for_blue:
            frame = cv2.circle(frame,i, 5, (255,0,0), -1)
    return img , frame



vid = cv2.VideoCapture(0)
#red Ranges
lower_red = np.array([160, 120, 100])
upper_red = np.array([179, 255, 255])

#blue Ranges
lower_blue = np.array([100, 90, 40])
upper_blue = np.array([130, 255, 255])

#green Ranges
lower_green = np.array([75, 30, 62])
upper_green = np.array([95, 200, 200])

while True:
    cnt = []
    co_ordinate_for_mouse = []
    co_ordinate_for_green = []
    co_ordinate_for_blue = []
    _ , frame = vid.read()

    frame = cv2.flip(frame , 1)
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    #red
    color = 'red'
    mask = cv2.inRange(hsv , lower_red , upper_red)
    contours , hierarchy = find_contours()
    img , frame= draw_contours(contours  , frame , color)  

    #blue
    color = 'blue'
    mask = cv2.inRange(hsv , lower_blue , upper_blue)
    contours , hierarchy = find_contours()
    img , frame= draw_contours(contours  , frame , color)  

    #green
    color = 'green'
    mask = cv2.inRange(hsv , lower_green , upper_green)
    contours , hierarchy = find_contours()
    img , frame= draw_contours(contours  , frame , color)  


    cv2.imshow("frame" , frame)
    #cv2.imshow("Mask" , mask)
    #cv2.imshow("img" , img)
    

    #Mouse Functions

    #1) MOVE CURSOR
    if len(co_ordinate_for_mouse) != 0 :
        mouse.move(co_ordinate_for_mouse[0][0] * 4.3 , co_ordinate_for_mouse[0][1] * 2.8 , absolute=True, duration=0)
    # 2) CLICK
    if dist() < 200:
        pyautogui.click(pyautogui.position()) 
    # 3) SCROLL
    if (len(co_ordinate_for_green) and len(co_ordinate_for_blue)) == 0 :
        pass
    else:
        if co_ordinate_for_green[0][1]- co_ordinate_for_blue[0][1] < 0 :
            pyautogui.scroll(10) 
        elif co_ordinate_for_green[0][1]- co_ordinate_for_blue[0][1] > 0 :
            pyautogui.scroll(10) 




    if cv2.waitKey(1) & 0xff == ord('q'):
        break


cv2.destroyAllWindows()
