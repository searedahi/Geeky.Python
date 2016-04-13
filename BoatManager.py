import time
import ThermometerService
import LocatorService


print('startingServices')

Tempy = ThermometerService.ThermometerService()
Loco = LocatorService.LocatorService()

print('loop')
while True:
    print('Temperature {0}').format(Tempy.CurrentFarenheight())
    print('Zulu Time   {0} ').format(Loco.getZuluTime())
    print('Position    {0} Lat x {1} Lon').format(Loco.getLatitude(),Loco.getLongitude())
    time.sleep(15)
    pass
