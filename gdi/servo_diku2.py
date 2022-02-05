######################################################
### 0 to 180 degree & 180 to 0 degree control per 1% (3 times) ###
######################################################

import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

for i in range (0,3) :    
    for high_time in range (30, 125):
        pwm.ChangeDutyCycle(high_time/10.0) 
        time.sleep(0.02)
 
    for high_time in range (125, 30,-1):
        pwm.ChangeDutyCycle(high_time/10.0)
        time.sleep(0.02)
        
pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()



