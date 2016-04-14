import time
import ThermometerService
import LocatorService


print('Starting Boat Manager')

Tempy = ThermometerService.ThermometerService()
Loco = LocatorService.LocatorService()

while Loco.gpsData is None:
    print('No location fix')
    time.sleep(5)

while True:
    print('Zulu Time   {0} ').format(Loco.getZuluTime())
    print('Temperature {0} Degrees F').format(Tempy.CurrentFarenheight())    
    print('Position    {0} Lat x {1} Lon').format(Loco.getLatitude(),Loco.getLongitude())
    time.sleep(6)
    pass
