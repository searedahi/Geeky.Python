import gps
import DataOps
import time
import threading

class LocatorService(object):
    """All the gps related logic for my geeky pi"""
    runBackgroundLocationThread = True

    session = gps.gps('localhost','2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    gpsData = None
    
    LastLat = '00.00'
    LastLon = '00.00'
    LastSpeed = '0.0'
    LastTrack = '0.0'

    def getSatelliteData(self):
        rawGpsData = self.session.next()
        if rawGpsData['class'] == 'TPV':
            self.gpsData = rawGpsData
        return self.gpsData

    def ParseTimeFromGpsData(self, argGpsData):
        if argGpsData is None:
            localGpsData = argGpsData
        else:
            localGpsData = self.gpsData

        gpsTime = '00:00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'time'):
                gpsTime = localGpsData.time
        return gpsTime

    def ParseLatitudeFromGpsData(self, argGpsData):
        if argGpsData is None:
            localGpsData = argGpsData
        else:
            localGpsData = self.gpsData

        gpsLat = '00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'lat'):
                gpsLat = localGpsData.lat
        return gpsLat

    def ParseLongitudeFromGpsData(self, argGpsData):
        if argGpsData is None:
            localGpsData = argGpsData
        else:
            localGpsData = self.gpsData

        gpsLon = '00.00'
        if localGpsData is not None:
            if hasattr(localGpsData, 'lon'):
                gpsLon = localGpsData.lon
        return gpsLon

    def ParseSpeedFromGpsData(self, argGpsData):
        if argGpsData is None:
            localGpsData = argGpsData
        else:
            localGpsData = self.gpsData

        gpsSpeed = '0.0'
        if localGpsData is not None:
            if hasattr(localGpsData, 'speed'):
                gpsSpeed = localGpsData.speed
        return gpsSpeed

    def ParseTrackFromGpsData(self, argGpsData):
        if argGpsData is None:
            localGpsData = argGpsData
        else:
            localGpsData = self.gpsData
        gpsTrack = '0.0'
        if localGpsData is not None:
            if hasattr(localGpsData, 'track'):
                gpsTrack = localGpsData.track
        return gpsTrack

    def CurrentTime(self):
        return self.CurrentTime(self.gpsData)

    def CurrentLatitude(self):
        return self.ParseLatitudeFromGpsData(self.gpsData)

    def CurrentLongitude(self):
        return self.ParseLongitudeFromGpsData(self.gpsData)

    def CurrentSpeed(self):
        return self.ParseSpeedFromGpsData(self.gpsData)

    def CurrentTrack(self):
        return self.ParseTrackFromGpsData(self.gpsData)

    def run(self):
            while self.runBackgroundLocationThread:
                #this should be the only call to the gps reciever in the entire project!
                loopGpsData = self.getSatelliteData()

                loopLat = self.ParseLatitudeFromGpsData(self,loopGpsData)
                loopLon = self.ParseLongitudeFromGpsData(self,loopGpsData)
                loopSpeed = self.ParseSpeedFromGpsData(self,loopGpsData)
                loopTrack = self.ParseTrackFromGpsData(self,loopGpsData)

                #did we change?
                if self.LastLat != loopLat\
                or self.LastLon != loopLon\
                or self.LastSpeed != loopSpeed\
                or self.LastTrack != loopTrack:
                    dbRepo = DataOps.DataOps()
                    dbRepo.saveGpsData(self.gpsData)
                    self.LastLat = loopLat
                    self.LastLon = loopLon
                    self.LastSpeed = loopSpeed
                    self.LastTrack = loopTrack
                time.sleep(5)
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
