import gps
import DataOps
import time
import threading

class LocatorService(object):
    """All the gps related logic for my pi"""
    runBackgroundLocationThread = True

    session = gps.gps('localhost','2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    gpsData = None
    
    LastLat = '00.00'
    LastLon = '00.00'

    def getSatelliteData(self):
        rawGpsData = self.session.next()
        if rawGpsData['class'] == 'TPV':
            self.gpsData = rawGpsData
        return self.gpsData

    def getZuluTime(self):
        localGpsData = self.gpsData
        gpsTime = '00:00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'time'):
                gpsTime = localGpsData.time
        return gpsTime

    def getLatitude(self):
        localGpsData = self.gpsData
        gpsLat = '00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'lat'):
                gpsLat = localGpsData.lat
        return gpsLat

    def getLongitude(self):
        localGpsData = self.gpsData
        gpsLon = '00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'lon'):
                gpsLon = localGpsData.lon
        return gpsLon

    def getSpeed(self):
        localGpsData = self.gpsData
        gpsSpeed = '0.0'
        if localGpsData is not None:
            if hasattr(localGpsData, 'speed'):
                gpsSpeed = localGpsData.speed
        return gpsSpeed

    def getTrack(self):
        localGpsData = self.gpsData
        gpsTrack = '0.0'
        if localGpsData is not None:
            if hasattr(localGpsData, 'track'):
                gpsTrack = localGpsData.track
        return gpsTrack

    def run(self):
            while self.runBackgroundLocationThread:
                loopGpsData = self.getSatelliteData()
                loopLat = self.getLatitude()
                loopLon = self.getLongitude()
                if self.LastLat != loopLat  or self.LastLon != loopLon:
                    dbRepo = DataOps.DataOps()
                    dbRepo.saveGpsData(self.gpsData)
                    self.LastLat = loopLat
                    self.LastLon = loopLon
                    print('Saved gpsData')
                #print(self.gpsData)
                time.sleep(8)
                pass
            return


    def __init__(self, interval=3):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        return
