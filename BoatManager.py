import DataOps
import ThermometerService
import TrollerService
import LocatorService


class BoatManager(object):
    """this is the master task that calls into the other python libs"""

    thermoSvc = ThermometerService()

    print(thermoSvc.CurrentFarenheight())