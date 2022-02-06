#-*- coding:utf-8 -*-
import re

import RPi.GPIO as GPIO
import time
servo_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
angle = 4.5
pwm.start(angle) 

import socket

# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '192.168.10.37'  
# 서버에서 지정해 놓은 포트 번호입니다. 
PORT = 9999       

# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))

try :
	direction = 1
	while True:
		direction *= -1
		client_socket.sendall('RPi : center position?'.encode())
		data = client_socket.recv(1024)
		decoded = repr(data.decode())
		print('Received', decoded)
	
		if decoded == "u'Close'":
			print('[Client CLOSE!!]')
			client_socket.close()
			break
		else :
			print('[Client RCV] : ', decoded)
			tmp_sub = re.split(u'\s|\u200b', decoded)
			#for id, val in enumerate(tmp_sub):
			#	print(id, val)
                        tmp_sub2 = tmp_sub[0].split(',')
			tmp = tmp_sub2[0].split("'")
			print('RAW:', tmp)
			tmp_x = int(tmp[1])
			#tmp.y = int(tmp[3])
			if tmp_x < 220:
				direction = 1
				print('Motor Right')
			elif tmp_x > 440:
				direction = -1
				print('Motor Left')
			else:
				direction = 0
				print('Motor Hold')

			if angle < 7.7 and angle > 3:
				if direction != 0:
					angle = angle + (0.1 * direction)
					pwm.ChangeDutyCycle(angle)

			print('Current Angle = ', angle)
			time.sleep(2)
	pwm.stop()
	GPIO.cleanup()
except:
	pwm.stop()
	GPIO.cleanup()
	print('Client Exception!')

