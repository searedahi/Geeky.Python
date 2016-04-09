import gps
import DataOps

class LocatorService(object):
    """All the gps related logic for my pi"""
    session = gps.gps('localhost','2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    CurrentTime = "00:00.00"
    CurrentLat = 000.000000
    CurrentLon = 000.000000
    CurrentSpeed = 000.000000
    CurrentHeading = 000.000000

    def getLocationData():
        gpsData = session.next()
        #save_object(gpsData, 'gpsDataOuput.pk1')
        if gpsData['class'] == 'TPV':
            if hasattr(gpsData, 'time'):
                gpsTime = gpsData.time
                CurrentTime = gpsTime
        return

    while True:
        DataOps.DataOps.saveGpsData()
        time.sleep(15)