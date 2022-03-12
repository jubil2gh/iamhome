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
global b_1st
b_1st = True

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
      if cur_angle <= 600 or cur_angle >= 1300: #500 = 0 deg, 2500 = 180 deg
        cur_angle -= delta
      pi.set_servo_pulsewidth(servo_pin, cur_angle)
      time.sleep(2.2)
    
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import datetime
import os
import numpy as np
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

zero_cam_angle()

cur_dir = os.getcwd() + '\\'

WINDOW_NAME = 'Full Integration'
cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)
cap.set(3,480)
cap.set(4,320)

time.sleep(0.1)

font = cv2.FONT_HERSHEY_SIMPLEX

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, img = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    img = cv2.flip(img, -1)
    img.flags.writeable = False
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_detection.process(img)

    # Draw the face detection annotations on the image.
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if faces.detections != None:
      num_of_faces = len(faces.detections)
      print('Num of OBJ : ', num_of_faces)
      global no_face_cnt

      if num_of_faces == 1:
        for detection in faces.detections:
          mp_drawing.draw_detection(img, detection)
          xmin = int(np.round(detection.location_data.relative_bounding_box.xmin*480, 2))
          ymin = int(np.round(detection.location_data.relative_bounding_box.ymin*320, 2))
          width = np.round(detection.location_data.relative_bounding_box.width*480, 2)
          height = np.round(detection.location_data.relative_bounding_box.height*320, 2)
          print('hori : ', xmin, width)
          print('vert : ', ymin, height)
          obj_center_x = int((xmin+width)-(width/2))
          TEXT = '{}'.format(obj_center_x-240)
          cv2.putText(img,TEXT,(xmin, ymin),font, 1, (0,255,0),2)
          print('Obj Center Pos = ', obj_center_x)
          change_cam_angle(obj_center_x)
          no_face_cnt = 0

      elif num_of_faces > 1:
          print('Multi Targets')

    else :
      no_face_cnt += 1
      if no_face_cnt > 18000: # 10 hz * 1800 sec(30min)
        zero_cam_angle()
  
    cv2.imshow(WINDOW_NAME, img)

#    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    key = cv2.waitKey(1)
    
    if key == 27:
        break
        
cap.release()
cv2.destroyAllWindows()

pi.stop()

