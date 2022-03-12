# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:58:30 2022

@author: 김관형
"""

from flask import Flask, render_template, Response
import cv2
import os
import time

WINDOW_NAME = 'Ai-FaceTracker'
font = cv2.FONT_HERSHEY_SIMPLEX
face_cascade = cv2.CascadeClassifier('./imported_model/haarcascade_frontalface_default.xml')

app = Flask(__name__)

# **********************{ Motor Ctrl }******************** #

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
      if cur_angle <= 600 or cur_angle >= 1300: #500 = 0 deg, 2500 = 180 deg
        cur_angle -= delta
      pi.set_servo_pulsewidth(servo_pin, cur_angle)
      time.sleep(1)
""" 
def zero_cam_angle():
    print('zero cam angle')

def change_cam_angle(pos):
    print('change cam angel')
"""
# ********************** { End of Motor Ctrl } *********************
zero_cam_angle()

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

def gen_frames():  # generate frame by frame from camera
    global no_face_cnt
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        frame = cv2.flip(frame, -1)

        if not success:
            break
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.08, 5) 
            num_of_face = len(faces)   
            print('Num of OBJ : ', num_of_face)
            if num_of_face == 0:
                no_face_cnt += 1
                if no_face_cnt > 18000: # 10 hz * 1800 sec(30min)
                    zero_cam_angle()

            elif num_of_face == 1:
                for x, y, w, h in faces:
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
                    print('OBJ POS : ', x, y)
                    if x:
                        # obj_center_x = int((x+w)-(w/2))
                        obj_center_x = int((x+w)-(w/2))
                        #obj_center_y = 0 #int((y+h)-(h/2))
                        TEXT = '{}'.format(obj_center_x-240)
                        cv2.putText(frame,TEXT,(x, y),font, 1, (0,255,0),2)
                        print('Obj Center Pos = ', obj_center_x)
                        change_cam_angle(obj_center_x)
                        no_face_cnt = 0
        
            else:
                print('Multi-targets')
        
            cv2.imshow(WINDOW_NAME, frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)