"""all the data operatiosn to boat pi"""

import sqlite3
import os
import uuid

#VS debugger
import ptvsd
ptvsd.enable_attach(secret='DataOps')

class DataOps(object):
    """all the data operations to boat pi"""
    
    serial_num = "0000000000000000"


    def dict_factory(cursor, row):
        """return a dictionary from a  row set"""
        result = {}
        for idx, col in enumerate(cursor.description):
            result[col[0]] = row[idx]
        return result

    def save_hit(self, sensorid):
        """save a troller hit to the database"""
        print('RUNNING {0} UNDER {1}').format("save_hit", self.serial_num)
        curs = self.conn.cursor()
        dbstr = '''INSERT INTO Hits(Id,SensorId,Date,DeviceId) \
        VALUES('{0}',{1},datetime('now'),'{2}');'''\
            .format(uuid.uuid4(), sensorid, self.serial_num)
        curs.execute(dbstr)
        self.conn.commit()
        return

    def save_temperature(self, sensortemp):
        """save a temperature record to the database"""
        print('RUNNING {0} UNDER {1}').format("save_temperature", self.serial_num)
        curs = self.conn.cursor()
        dbstr = '''INSERT INTO Temperatures(Id,SensorReading,Date,DeviceId) \
        VALUES('{0}',{1},datetime('now'),'{2}');'''\
            .format(uuid.uuid4(), sensortemp, self.serial_num)
        curs.execute(dbstr)
        self.conn.commit()
        return

    def save_gps_data(self, gpsdata):
        """save a location to the database"""
        print('RUNNING {0} UNDER {1}').format("save_gps_data", self.serial_num)

        try:
            if gpsdata.lat != None\
            or gpsdata.lon != None\
            or gpsdata.speed != None\
            or gpsdata.track != None:

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
        except :            
            print(gpsdata)
            pass

        return

    def get_gps_datum(self):
        """get all the gps data from the database"""
        print('RUNNING {0} UNDER {1}').format("get_gps_datum", self.serial_num)
        curs = self.conn.cursor()
        dbstr = '''SELECT Id,Lat,Lon,Speed,Track,Date,DeviceId FROM Locations ORDER BY Date DESC;'''
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

    def get_gps_data(self, recordid):
        """get the gps record by id from the database"""
        print('RUNNING {0} UNDER {1}').format("get_gps_data", self.serial_num)

        curs = self.conn.cursor()
        dbstr = '''SELECT * FROM Locations WHERE Id = {0};'''.format(recordid)
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows


    def get_temperatures(self):
        """get all the temperatures from the database"""
        print('RUNNING {0} UNDER {1}').format("get_gps_datum", self.serial_num)
        curs = self.conn.cursor()
        dbstr = '''SELECT Id, SensorReading, Date, DeviceId FROM Temperatures ORDER BY Date DESC;'''
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

    def get_temperature(self, recordid):
        """get the temperature record by id from the database"""
        print('RUNNING {0} UNDER {1}').format("get_gps_data", self.serial_num)

        curs = self.conn.cursor()
        dbstr = '''SELECT Id, SensorReading, Date, DeviceId FROM Temperatures WHERE Id = {0};'''.format(recordid)
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

    def get_temperatures_above_date(self, date):
        """get all the temperatures from the database"""
        print('RUNNING {0} UNDER {1}').format("get_gps_datum", self.serial_num)
        curs = self.conn.cursor()
        dbstr = '''SELECT Id, SensorReading, Date, DeviceId FROM Temperatures WHERE Date > {0} ORDER BY Date DESC;'''.format(date)
        curs.execute(dbstr)
        rows = curs.fetchall()
        return rows

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

    conn = sqlite3.connect('tester.db', check_same_thread=False)
    conn.row_factory = dict_factory

    def __init__(self, serial = None):

        if serial is None:
            self._getserial_()
        else:
            self.serial_num = serial

    def __delattr__(self, attr):
        self.conn.close()
