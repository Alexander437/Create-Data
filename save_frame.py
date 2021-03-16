"""Модуль содержит класс для формирования базы данных"""

import time
import os
import argparse

import cv2

class SaveFrame():
    """Класс предназначен для создания базы данных для обучения нейросети
    
    Конструктор принимает номер порта, к которому подключена камера.
    Режим сохранения кадров будет включаться и выключаться при нажатии 'R'
    Для выхода нажмите 'Q'"""

    def __init__(self, camera_port=0):
        self.camera_port = camera_port
        self.mode = 0

    def __call__(self, label, delay=20, out='images'):
        """Метод для сохранения кадров"""
        cap = cv2.VideoCapture(self.camera_port)
        count = 0
        count_frame = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            path_base = os.path.join(out, (label + '_') )
            if (self.mode%2 == 1):
                count_frame += 1
                if (count_frame%delay == 0):
                    path = path_base + str(count) + '.jpeg'
                    cv2.imwrite(path, frame)
                    path = path_base + str(count+1) + '.jpeg'
                    cv2.imwrite(path, self.augmentation(frame, 10))
                    path = path_base + str(count+2) + '.jpeg'
                    cv2.imwrite(path, self.augmentation(frame, 15))
                    path = path_base + str(count+3) + '.jpeg'
                    cv2.imwrite(path, self.augmentation(frame, -15))
                    print('writing img: ', path)
                    count += 4

            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)

            if key == ord('r'):
                self.mode += 1
                time.sleep(1)
            if key == ord('q'):
                self.mode = 0
                break

        cap.release()
        cv2.destroyAllWindows()

    def augmentation(self, img, grad):
        """Метод для расширения базы данных путем поворота кадров"""
        rows,cols,cannels = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),grad,1)

        path = 'images/img.jpeg'
        dst = cv2.warpAffine(img,M,(cols,rows))
        return(cv2.resize(dst[50:430, 85:540, :], (640,480)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Программа save_frame.py предназначена для\n"
                                                "формирования базы данных для обучения нейросети")
    parser.add_argument('--label', help='Класс (рек. enemy или friend)', default="enemy")
    parser.add_argument('--delay', help='Какой кадр сохр.', default=20)
    parser.add_argument('--output', help='Путь к сохр. кадрам (по умолчанию images)', default='images')
    parser.add_argument('--cam_port', type=int, help='Номер порта, к кот. подключена камера', default=0)
    args = parser.parse_args()

    sf = SaveFrame(camera_port=args.cam_port)
    sf(label=args.label, delay=int(args.delay), out=args.output)

