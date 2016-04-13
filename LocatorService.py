import gps
import DataOps
import time
import threading

class LocatorService(object):
    """All the gps related logic for my pi"""
    runBackgroundLocationThread = True

    session = gps.gps('localhost','2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    gpsData = []
    
    def getSatelliteData(self):
        self.gpsData = self.session.next()
        #save_object(gpsData, 'gpsDataOuput.pk1')
        #print(gpsData)
        return self.gpsData

    def getZuluTime(self):
        localGpsData = self.gpsData
        gpsTime = '00:00.00'
        if localGpsData['class'] == 'TPV':
            if hasattr(localGpsData, 'time'):
                gpsTime = localGpsData.time
        return gpsTime

    def getLatitude(self):
        localGpsData = self.gpsData
        gpsLat = '00.00'
        if localGpsData['class'] == 'TPV':
            if hasattr(localGpsData, 'lat'):
                gpsLat = localGpsData.lat
        return gpsLat

    def getLongitude(self):
        localGpsData = self.gpsData
        gpsLon = '00.00'
        if localGpsData['class'] == 'TPV':
            if hasattr(localGpsData, 'lon'):
                gpsLon = localGpsData.lon
        return gpsLon

    def getSpeed(self):
        localGpsData = self.gpsData
        gpsSpeed = '0.0'
        if localGpsData['class'] == 'TPV':
            if hasattr(localGpsData, 'speed'):
                gpsSpeed = localGpsData.speed
        return gpsSpeed

    def getHeading(self):
        localGpsData = self.gpsData
        gpsHeading = '0.0'
        if localGpsData['class'] == 'TPV':
            if hasattr(localGpsData, 'heading'):
                gpsHeading = localGpsData.heading
        return gpsHeading

    def run(self):
            while self.runBackgroundLocationThread:
                self.getSatelliteData()
                #dbRepo = DataOps.DataOps()
                #dbRepo.saveGpsData()
                #print(self.gpsData)
                time.sleep(10)
                pass
            return


    def __init__(self, interval=6):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        return
