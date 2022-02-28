# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:09:19 2021

@author: natha
"""
import time
import pigpio
servo_pin = 21
global force_angle 
force_angle = 0

pi = pigpio.pi()

def zero_cam_angle():
    global cur_angle
    global force_angle
    if force_angle == 0:
      cur_angle = 1000 #front
    elif force_angle == 1:
      cur_angle = 1100 #window
    else :
      cur_angle = 900 #desk

    pi.set_servo_pulsewidth(servo_pin, cur_angle)  

    global no_face_cnt
    no_face_cnt = 0

    force_angle += 1
    if force_angle == 3:
      force_angle = 0
      
def change_cam_angle(pos):
    delta = pos - 240
    if abs(delta) > 60:
      if delta < 0: delta = 30
      else: delta = -1*30
      
      global cur_angle
      cur_angle += delta 
      if cur_angle <= 600 or cur_angle >= 1500: #500 = 0 deg, 2500 = 180 deg
        cur_angle -= delta
      pi.set_servo_pulsewidth(servo_pin, cur_angle)
      time.sleep(1)
    
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import datetime
import os

zero_cam_angle()

cur_dir = os.getcwd() + '\\'

WINDOW_NAME = 'Full Integration'
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = PiCamera()
cap.resolution = (480, 320)
cap.framerate = 10
rawCapture = PiRGBArray(cap, size=(480, 320))

time.sleep(0.1)

face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_frontalface_default.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_eye.xml')
# face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_lefteye_2splits.xml')

font = cv2.FONT_HERSHEY_SIMPLEX

for frame in cap.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    img = cv2.flip(img, -1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.08, 5)    
    #print('Num of OBJ : ', len(faces))
    if len(faces) == 0:
      global no_face_cnt
      no_face_cnt += 1
      if no_face_cnt > 18000: # 10 hz * 1800 sec(30min)
        zero_cam_angle()
        
    for x, y, w, h in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
        print('OBJ POS : ', x, y)
        if x:
          # obj_center_x = int((x+w)-(w/2))
          obj_center_x = int((x+w)-(w/2))
          #obj_center_y = 0 #int((y+h)-(h/2))
          TEXT = '{}'.format(obj_center_x-240)
          cv2.putText(img,TEXT,(x, y),font, 1, (0,255,0),2)
          print('Obj Center Pos = ', obj_center_x)
          change_cam_angle(obj_center_x)
          no_face_cnt = 0
  
    cv2.imshow(WINDOW_NAME, img)
    rawCapture.truncate(0)
    
#    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(1)
    
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()

pi.stop()

