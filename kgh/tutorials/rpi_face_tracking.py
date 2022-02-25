# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:09:19 2021

@author: natha
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import datetime
import os

cur_dir = os.getcwd() + '\\'

cap = PiCamera()
rawCapture = PiRGBArray(cap)
time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_eye.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_lefteye_2splits.xml')

while True:
    cap.capture(rawCapture, format='bgr')
    img = rawCapture.array
    
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
        
cap.release()
cv2.destroyAllWindows()
        