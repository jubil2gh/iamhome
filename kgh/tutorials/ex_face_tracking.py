# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:09:19 2021

@author: natha
"""

import cv2
import datetime
import os

cur_dir = os.getcwd() + '\\'

cap = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
record = False

face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_eye.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_lefteye_2splits.xml')

while True:
    ret, img = cap.read()
    
    if not ret:
        break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.08, 5)    
    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
        
    cv2.imshow('Output', img)
    
    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(33)
    
    if key == 27:
        break
    elif key == ord('c'):
        print('Capture')
        cv2.imwrite(cur_dir + str(now) + ".png", img)
    elif key == ord('s'):
        print("Video Rec Start")
        record = True
        video = cv2.VideoWriter(cur_dir + str(now) + ".avi", fourcc, 20.0, (img.shape[1], img.shape[0]))
    elif key == ord('t'):
        print("Video Rec Stop")
        record = False
        video.release()

    if record == True:
        print("On Rec..")
        video.write(img)
        
cap.release()
cv2.destroyAllWindows()
        