import RPi.GPIO as GPIO
import time
import DataOps

tm = time.time()
poleMap = [11,13,15,16,18]
timestamps = [tm,tm,tm,tm,tm]

def knockDown(pin):
        idx = poleMap.index(pin)
        time_now = time.time()
        time_then = timestamps[idx]
        if(time_now - time_then) >= 3:
            DataOps.DataOps.saveHit(idx + 1)
        timestamps[idx] = time_now                
        return


GPIO.setmode(GPIO.BOARD)

#setup the pins and callbacks
for pole in poleMap:
    GPIO.setup(pole,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pole, GPIO.FALLING, callback=knockDown)
    pass
     
while True:
    time.sleep(1)
    pass