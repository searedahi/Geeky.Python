""" Location operations and central gps sensor access. """
import gps
import time
import threading

#import ptvsd
#ptvsd.enable_attach(secret='LocatorService')
import DataOps



class LocatorService(object):
    """All the gps related logic for my geeky pi"""
    RUN_BACKGROUND = True

    session = gps.gps('localhost', '2947')
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    
    
    
    serialNum = DataOps.DataOps()
    SERIALNUM = serialNum.serial_num

    gps_data = None

    last_lat = '00.00'
    last_lon = '00.00'
    last_speed = '0.0'
    last_track = '0.0'

    def _get_satellite_data_(self):
        """ Get the raw satellite data from gps and store in class variable. """
        raw_signal = self.session.next()
        if raw_signal['class'] == 'TPV':
            self.gps_data = raw_signal
        return self.gps_data

    def _time_from_gps_data_(self, arg_data=None):
        """ Parse the zulu time from the raw satellite data. """

        if arg_data is None:
            local_data = self.gps_data
        else:
            local_data = arg_data

        gps_time = '00:00.00'
        if local_data is not None:
            if hasattr(local_data, 'time'):
                gps_time = local_data.time
        return gps_time

    def _latitude_from_gps_data_(self, arg_data=None):
        """ Parse the latitude from the raw satellite data. """
        if arg_data is None:
            local_data = self.gps_data
        else:
            local_data = arg_data

        gps_lat = '00.00'
        if local_data is not None:
            if hasattr(local_data, 'lat'):
                gps_lat = local_data.lat
        return gps_lat

    def _longitude_from_gps_data_(self, arg_data=None):
        """ Parse the longitude from the raw satellite data. """
        if arg_data is None:
            local_data = self.gps_data
        else:
            local_data = arg_data

        gps_lon = '00.00'
        if local_data is not None:
            if hasattr(local_data, 'lon'):
                gps_lon = local_data.lon
        return gps_lon

    def _speed_from_gps_data_(self, arg_data=None):
        """ Parse the speed from the raw satellite data. """
        if arg_data is None:
            local_data = self.gps_data
        else:
            local_data = arg_data

        gps_speed = '0.0'
        if local_data is not None:
            if hasattr(local_data, 'speed'):
                gps_speed = local_data.speed
        return gps_speed

    def _track_from_gps_data_(self, arg_data=None):
        """ Parse the track from the raw satellite data. """
        if arg_data is None:
            local_data = self.gps_data
        else:
            local_data = arg_data

        gps_track = '0.0'
        if local_data is not None:
            if hasattr(local_data, 'track'):
                gps_track = local_data.track
        return gps_track

    def current_time(self):
        """ The last known time. """
        return self._time_from_gps_data_()

    def current_latitude(self):
        """ The last known latitude. """
        return self._latitude_from_gps_data_()

    def current_longitude(self):
        """ The last known logitude. """
        return self._longitude_from_gps_data_()

    def current_speed(self):
        """ The last known speed. """
        return self._speed_from_gps_data_()

    def current_track(self):
        """ The last known track. """
        return self._track_from_gps_data_()

    def _run_(self):
        """ The background operations of the service. """
        while self.RUN_BACKGROUND:
            #this should be the only call to the gps reciever in the entire
            #project!
            loop_data = self._get_satellite_data_()

            loop_lat = self._latitude_from_gps_data_(loop_data)
            loop_lon = self._longitude_from_gps_data_(loop_data)
            loop_speed = self._speed_from_gps_data_(loop_data)
            loop_track = self._track_from_gps_data_(loop_data)

            #did we change?
            if self.last_lat != loop_lat\
            or self.last_lon != loop_lon\
            or self.last_speed != loop_speed\
            or self.last_track != loop_track:
                gps_db = DataOps.DataOps(self.SERIALNUM)
                gps_db.save_gps_data(loop_data)
                self.last_lat = loop_lat
                self.last_lon = loop_lon
                self.last_speed = loop_speed
                self.last_speed = loop_track
            time.sleep(5)
        return

    def __init__(self, interval=3):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self._run_, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        return
