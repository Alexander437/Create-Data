import cv2
import numpy as np

drawing = False

ix,iy = -1,-1

def write_in_file(x0, y0, x1, y1):
    out_file = open("images/annotations", "a")
    s = 'enemy_0.jpeg'+', '+str(x0)+', '+str(y0)+', '+str(x1)+', '+str(y1)+'\n'
    print(s)
    out_file.write(s)

def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y

    elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),1)
            write_in_file(ix, iy, x, y)

img = cv2.imread('images/enemy_0.jpeg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
       break
cv2.destroyAllWindows()
