"""
The main scope for all BoatPy tasks.
"""
import time
import ptvsd

import ThermometerService
import LocatorService
import GeekyServer


ptvsd.enable_attach(secret='BoatManager')

print('Starting Boat Manager')

TEMPSVC = ThermometerService.ThermometerService()
LOCASVC = LocatorService.LocatorService()
WWWSVC = GeekyServer.ApiServer(TEMPSVC, LOCASVC)

while LOCASVC.gps_data is None:
    print('Aquiring Satellites')
    time.sleep(5)

while True:
    print('Zulu Time   {0} ').format(LOCASVC.current_time())
    print('Temperature {0} Degrees F').format(TEMPSVC.current_farenheight())
    #print('Position    {0} Lat x {1} Lon').format(Loco.CurrentLatitude(),Loco.CurrentLongitude())
    time.sleep(6)
