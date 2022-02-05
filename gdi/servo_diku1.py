###############################
### 0/90/180 degree control ###
###############################

import RPi.GPIO as GPIO
import time
servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz
pwm.start(3.0) # 20ms x 3.0% = 0.6ms (0 degree)

for cnt in range(0, 2) :       # 3 times repeat
    pwm.ChangeDutyCycle(3.3)   # 0 degree
    time.sleep(1.0)            # servo motor delay time
    pwm.ChangeDutyCycle(8.0)   # 90 degree
    time.sleep(1.0)            # servo motor delay time
    pwm.ChangeDutyCycle(12.5)  # 180 degree
    time.sleep(1.0)            # servo motor delay time
    pwm.ChangeDutyCycle(8.0)   # 90 degree
    time.sleep(1.0)            # servo motor delay time
    
pwm.ChangeDutyCycle(3.3)
time.sleep (1.5)

# pwm.stop()
# GPIO.cleanup()


#####################################
### 0/45/90/135/180 dgree control ###
#####################################


timeA = 0.6

for cnt in range(0, 2) :       
    pwm.ChangeDutyCycle(3.0)   # 0 degree
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(5.5)   # 45 degre
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(7.5)   # 90 degree
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(9.5)   # 135 degree
    time.sleep(timeA)          # servo motor delay time    
    pwm.ChangeDutyCycle(12.5)  # 180 degree
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(9.5)   # 135 degree
    time.sleep(timeA)          # servo motor delay time  
    pwm.ChangeDutyCycle(7.5)   # 90 degree
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(5.5)   # 서보 모터를 45도로 회전(이동)
    time.sleep(timeA)          # servo motor delay time
    pwm.ChangeDutyCycle(3.0)   # 0 degree
    time.sleep(timeA)          # servo motor delay time

pwm.ChangeDutyCycle(0.0)
time.sleep (1.5)

#pwm.stop()
#GPIO.cleanup()


######################################
### 0 to 180 degree control per 1% ###
######################################

#import RPi.GPIO as GPIO
#import time

#servo_pin = 18
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo_pin,GPIO.OUT)
#pwm = GPIO.PWM(servo_pin, 50)
#pwm.start(3.0)

for cnt in range(0, 2) :
    for high_time in range (30, 125):
        pwm.ChangeDutyCycle(high_time/10.0)  # for => No integer 
        time.sleep(0.02)
    
    pwm.ChangeDutyCycle(3.0)
    time.sleep(1.0)
    
pwm.ChangeDutyCycle(0.0)
time.sleep (1.5)

#pwm.stop()
#GPIO.cleanup()


##################################################################
### 0 to 180 degree & 180 to 0 degree control per 1% (3 times) ###
##################################################################

import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
#pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

for i in range (0,2) :    
    for high_time in range (30, 125):
        pwm.ChangeDutyCycle(high_time/10.0)  # for => No integer 
        time.sleep(0.02)
 
    for high_time in range (125, 30,-1):
        pwm.ChangeDutyCycle(high_time/10.0)  # for => No integer 
        time.sleep(0.02)
        
pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()
