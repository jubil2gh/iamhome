# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
servo_pin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

pwm.ChangeDutyCycle(3.0)
time.sleep(1.0)

pwm.stop()
GPIO.cleanup()
