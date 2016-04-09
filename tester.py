import RPi.GPIO as GPIO
import time
import threading
import sqlite3
import os
import glob
import gps

script, filename = argv

#GPS
session = gps.gps('localhost','2947')
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)


#SQL
conn = sqlite3.connect('tester.db')
curs = conn.cursor()

#Thermometer
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'



GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)

tm = time.time()
poleMap = [11,13,15,16,18]
timestamps = [tm,tm,tm,tm,tm]


try:
        def blink():
                if(GPIO.input(7) is True):
                        GPIO.output(7,False)                        
                else:
                        GPIO.output(7,True)                        
                return

        def save_object(obj, filename):
                with open(filename, 'wb') as output:
                        pickle.dump(obj,output,pickle.HIGHEST_PROTOCOL)

                
        def knockDown(pin):
                idx = poleMap.index(pin)
                time_now = time.time()
                time_then = timestamps[idx]
                if(time_now - time_then) >= 3:
                        gpsTime = '12:00.00'
                        gpsData = session.next()
                        #save_object(gpsData, 'gpsDataOuput.pk1')
                        if gpsData['class'] == 'TPV':
                                if hasattr(gpsData, 'time'):
                                        gpsTime = gpsData.time


                        
                        raw_temp = read_temp()
                        
                        print('Knockdown on pole {0}.  {1} Degrees F  at {2}'.format(idx + 1,farenheight_from_raw(raw_temp), gpsTime))
                timestamps[idx] = time_now                
                return

        def celcius_from_raw(raw):
                return float(raw) / 1000.0

        def farenheight_from_raw(raw):
                celcius = float(raw) / 1000.0
                return celcius * 9.0 / 5.0 + 32.0

        def read_temp_raw():
                f = open(device_file, 'r')
                lines = f.readlines()
                f.close()
                return lines

        def read_temp():
                lines = read_temp_raw()
                while lines[0].strip()[-3:] != 'YES':                       
                        lines = read_temp_raw()
                equals_pos = lines[1].find('t=')
                if equals_pos != -1:
                        temp_string = lines[1][equals_pos + 2:]
                        return temp_string






        GPIO.add_event_detect(11, GPIO.FALLING, callback=knockDown)
        GPIO.add_event_detect(13, GPIO.FALLING, callback=knockDown)
        GPIO.add_event_detect(15, GPIO.FALLING, callback=knockDown)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=knockDown)
        GPIO.add_event_detect(18, GPIO.FALLING, callback=knockDown)

             
        while True:
                pass
except:        
        print('Exited on except')
        pass

conn.close()
GPIO.cleanup()



        




