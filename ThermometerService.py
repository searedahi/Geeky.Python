import os
import glob
import time
import DataOps
import ptvsd

class ThermometerService(object):
    """all the data operatiosn to my pi"""

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    thermoData = DataOps.DataOps()
    lastTemperature = 0

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            return temp_string

    def CurrentCelcius(self):
        temp_string = lastTemperature
        temp_c = float(temp_string) / 1000.0
        return temp_c

    def CurrentFarenheight(self):
        temp_c = CurrentCelcius()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

    def runService(self):
        while True:
            rawTemp = self.read_temp()
            if rawTemp != self.lastTemperature:
                self.thermoData.saveTemperature(rawTemp)
                self.lastTemperature = rawTemp
            time.sleep(6)