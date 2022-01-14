# Import libraries
import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 11 as an output, and define as servo1 as PWM pin
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

angle1 = 0.0
angle2 = 180.0


def handleServo(status):
    if status == "open":
        servo1.ChangeDutyCycle(2+(angle1/18))
    elif staus == "close":
        servo1.ChangeDutyCycle(2+(angle2/18))

    time.sleep(0.5)
    servo1.ChangeDutyCycle(0)

