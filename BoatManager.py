import time
import ThermometerService
import LocatorService
import GeekyServer
import ptvsd
ptvsd.enable_attach(secret='BoatManager')

print('Starting Boat Manager')

Tempery = ThermometerService.ThermometerService()
Loco = LocatorService.LocatorService()
WebServ = GeekyServer.ApiServer()
WebServ.Tempy = Tempery

while Loco.gpsData is None:
    print('Aquiring Satellites')
    time.sleep(5)

while True:
    print('Zulu Time   {0} ').format(Loco.CurrentTime())
    print('Temperature {0} Degrees F').format(Tempery.CurrentFarenheight())    
    #print('Position    {0} Lat x {1} Lon').format(Loco.CurrentLatitude(),Loco.CurrentLongitude())
    time.sleep(6)
    pass
