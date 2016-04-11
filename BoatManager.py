import time

import DataOps
import ThermometerService
import TrollerService
import LocatorService


class BoatManager(object):
    """this is the master task that calls into the other python libs"""


    def __init__(self, **kwargs):
        thermoSvc = ThermometerService()

        while True:
            print(thermoSvc.CurrentFarenheight())
            print('hello')
            time.sleep(15)
            pass

