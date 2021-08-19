"""Модуль содержит класс для формирования границ рамок"""

import os

import cv2
import numpy as np

drawing = False

ix,iy = -1,-1

class Markup():
    """Класс предназначен для формирования границ рамок для обучения нейросети
    
    Конструктор принимает номер порта, к которому подключена камера.
    Режим сохранения кадров будет включаться и выключаться при нажатии 'R'
    Для выхода нажмите 'Q'"""
def __init__(self, root):
    self.root = root
    self.path_list = list()

def write_in_file(x0, y0, x1, y1, root):
    out_file = open(os.path.join(root, "annotations"), "a")
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
            write_in_file(ix, iy, x, y, root)

img = cv2.imread('images/enemy_0.jpeg')
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
       break
cv2.destroyAllWindows()


