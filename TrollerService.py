""" The service responsible for troller IO management """

import RPi.GPIO as GPIO
import time
import DataOps

NW = time.time()
POLES = [11, 13, 15, 16, 18]
TIMES = [NW, NW, NW, NW, NW]

def knock_down(pin):
    """ callback for when the troller gets knocked down """
    idx = POLES.index(pin)
    time_now = time.time()
    time_then = TIMES[idx]
    if(time_now - time_then) >= 3:
        localpin = idx + 1
        dataops = DataOps.DataOps()
        dataops.save_hit(localpin)
    TIMES[idx] = time_now
    return

GPIO.setmode(GPIO.BOARD)

#setup the pins and callbacks
for pole in POLES:
    GPIO.setup(pole, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pole, GPIO.FALLING, callback=knock_down)

while True:
    time.sleep(1)
