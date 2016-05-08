"""all the data operatiosn to my pi"""

import sqlite3
import os
import uuid

class DataOps(object):
    """all the data operatiosn to my pi"""

    @staticmethod
    def dict_factory(cursor, row):
        """return a dictionary from a  row set"""
        result = {}
        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]
        return result

    def save_hit(self, sensorid):
        """save a troller hit to the database"""
        curs = self.conn.cursor()
        dbstr = '''INSERT INTO Hits(Id,SensorId,Date,DeviceId) \
        VALUES('{0}',{1},datetime('now'),'{2}');'''\
            .format(uuid.uuid4(), sensorid, self.serial_num)
        curs.execute(dbstr)
        self.conn.commit()
        return

    def save_temperature(self, sensortemp):
        """save a temperature record to the database"""
        curs = self.conn.cursor()
        dbstr = '''INSERT INTO Temperatures(Id,SensorReading,Date,DeviceId) \
        VALUES('{0}',{1},datetime('now'),'{2}');'''\
            .format(uuid.uuid4(), sensortemp, self.serial_num)
        curs.execute(dbstr)
        self.conn.commit()
        return

    def save_gps_data(self, gpsdata):
        """save a location to the database"""
        curs = self.conn.cursor()
        dbstr = '''INSERT INTO Locations(Id,Lat,Lon,Speed,Track,Date,DeviceId) \
        VALUES('{0}',{1},{2},{3},{4},datetime('now'),'{5}');'''\
            .format(uuid.uuid4(),
                    gpsdata.lat,
                    gpsdata.lon,
                    gpsdata.speed,
                    gpsdata.track,
                    self.serial_num)
        curs.execute(dbstr)
        self.conn.commit()
        return

    def get_gps_datum(self):
        """get all the gps data from the database"""
        curs = self.conn.cursor()
        dbstr = '''SELECT Id,Lat,Lon,Speed,Track,Date,DeviceId FROM Locations;'''
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

    def get_gps_data(self, recordid):
        """get the gps record by id from the database"""
        curs = self.conn.cursor()
        dbstr = '''SELECT * FROM Locations WHERE Id = {0};'''.format(recordid)
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

    serial_num = "0000000000000000"
    conn = sqlite3.connect('tester.db', check_same_thread=False)
    conn.row_factory = dict_factory

    def _getserial_(self):
        """extract the serial number from the rapsberry pi"""
        cpuserial = "0000000000000001"
        try:
            pypath = '/proc/cpuinfo'
            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath, "..", "..", "..", pypath))
            target = open(filepath, "r")
            for line in target:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            target.close()
        except Exception as ex:
            print(ex)
            cpuserial = "ERROR000000004"
        self.serial_num = cpuserial
        return self.serial_num

    def __init__(self):
        self._getserial_()

    def __delattr__(self, attr):
        self.conn.close()
