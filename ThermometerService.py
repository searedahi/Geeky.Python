""" Thermomter operations and central sensor IO control. """

import os
import glob
import time
import threading

#import ptvsd
#ptvsd.enable_attach(secret='ThermometerService')
import DataOps

class ThermometerService(object):
    """all the data operatiosn to my pi"""

    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    BASEDIR = '/sys/bus/w1/devices/'
    DEVICE_FOLDER = glob.glob(BASEDIR + '28*')[0]
    DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'

    last_temp = 0
    RUN_BACKGROUND = True
    serialNum = DataOps.DataOps()
    SERIALNUM = serialNum.serial_num

    def _read_temp_raw_(self):
        """ get the raw sensor reading for the ds18b20 """
        local_f = open(self.DEVICE_FILE, 'r')
        lines = local_f.readlines()
        local_f.close()
        return lines

    def _read_temp_(self):
        """ callback for when the troller gets knocked down """
        lines = self._read_temp_raw_()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw_()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            sensor_temp_string = lines[1][equals_pos + 2:]
            return sensor_temp_string

    def current_celcius(self):
        """ The current temperature in celcius. """

        localtemp = self.last_temp
        temp_c = float(localtemp) / 1000.0
        return temp_c

    def current_farenheight(self):
        """ The current temperature in celcius. """

        temp_c = self.current_celcius()
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

    def run(self):
        """ Background service operation to monitor the temperature /
        and update LAST_TEMP of any changes. """

        while self.RUN_BACKGROUND:
            raw_temp = self._read_temp_()
            if raw_temp != self.last_temp:
                thermo_db = DataOps.DataOps(self.SERIALNUM)
                thermo_db.save_temperature(raw_temp)
                self.last_temp = raw_temp
            time.sleep(6) # it takes 4-6 seconds for the sensor to read and report back.

    def __init__(self, interval=4):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
