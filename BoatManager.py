import time
import ThermometerService
import LocatorService
import GeekySeaApi


print('Starting Boat Manager')

WebServ = GeekySeaApi.ApiServer()
Tempy = ThermometerService.ThermometerService()
Loco = LocatorService.LocatorService()



while Loco.gpsData is None:
    print('Aquiring Satellites')
    time.sleep(5)

while True:
    print('Zulu Time   {0} ').format(Loco.CurrentTime())
    print('Temperature {0} Degrees F').format(Tempy.CurrentFarenheight())    
    #print('Position    {0} Lat x {1} Lon').format(Loco.CurrentLatitude(),Loco.CurrentLongitude())
    time.sleep(6)
    pass
