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

WINDOW_NAME = 'Full Integration'
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = PiCamera()
cap.resolution = (480, 320)
cap.framerate = 32
rawCapture = PiRGBArray(cap, size=(480, 320))

time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_eye.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_lefteye_2splits.xml')

for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#    cap.capture(rawCapture, format='bgr')
    img = frame.array
    img = cv2.flip(img, -1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.08, 5)    
    print(faces)
    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
        
    cv2.imshow(WINDOW_NAME, img)
    rawCapture.truncate(0)
    
#    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(1)
    
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
        
