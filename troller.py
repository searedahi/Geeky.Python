import RPi.GPIO as GPIO
from time import sleep

var=1 

couter=0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(33,GPIO.OUT)
GPIO.output(33,1)

def callb(channel):
    if var == 1:
        print('movement')

GPIO.add_event_detect(11, GPIO.RISING, callback= callb, bouncetime=300)


while 1==1:
    pass
