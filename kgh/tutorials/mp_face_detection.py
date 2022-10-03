# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 19:18:56 2022

@author: 김관형
"""

import numpy as np
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

font = cv2.FONT_HERSHEY_SIMPLEX

# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image = cv2.flip(image, -1)
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    print('Num of OBJ : ', len(results.detections))
    if results.detections:
      for detection in results.detections:
        mp_drawing.draw_detection(image, detection)
        xmin = int(np.round(detection.location_data.relative_bounding_box.xmin*640, 2))
        ymin = int(np.round(detection.location_data.relative_bounding_box.ymin*480, 2))
        width = np.round(detection.location_data.relative_bounding_box.width*640, 2)
        height = np.round(detection.location_data.relative_bounding_box.height*480, 2)
        print('hori : ', xmin, width)
        print('vert : ', ymin, height)
        TEXT = '{},{}'.format(xmin, ymin)
        cv2.putText(image,TEXT,(xmin, ymin),font, 1, (0,255,0),2)
              
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()