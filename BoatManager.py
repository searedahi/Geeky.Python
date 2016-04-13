import time
import ThermometerService
import LocatorService


print('startingServices')

Tempy = ThermometerService.ThermometerService()
Loco = LocatorService.LocatorService()

print('loop')
while True:
    print('{0} Degrees F').format(Tempy.CurrentFarenheight())
    print('{0} Zulu Time').format(Loco.getZuluTime())
    print('{0} Latitude').format(Loco.getLatitude())
    time.sleep(15)
    pass