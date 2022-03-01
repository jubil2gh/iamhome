# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:23:37 2022

@author: 김관형
"""

import cv2
import numpy as np

# 비디오 파일 열기
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

# 배경 영상 등록
ret, back = cap.read()

if not ret:
    print('Background image registration failed!')
    sys.exit()

# back: uint8 배경, fback: float32 배경
# 흑백으로 변환
back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)
# 노이즈 제거
back = cv2.GaussianBlur(back, (0, 0), 1.0)
# float32로 변경
fback = back.astype(np.float32)

# 비디오 매 프레임 처리
while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (0, 0), 1.0)

    # fback: float32, back: uint8 배경
    # gray는 현재 프레임의 영상
    cv2.accumulateWeighted(gray, fback, 0.01)
    # absdiff 함수를 이용하기 위해 unit8로 변경
    back = fback.astype(np.uint8)

    # 인자의 타입이 같아야 한다.
    diff = cv2.absdiff(gray, back)
    _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # 레이블링을 이용하여 바운딩 박스 표시
    cnt, _, stats, _ = cv2.connectedComponentsWithStats(diff)

    for i in range(1, cnt):
        x, y, w, h, s = stats[i]

        if s < 100:
            continue

        cv2.rectangle(frame, (x, y, w, h), (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('diff', diff)
    cv2.imshow('back', back)

    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()