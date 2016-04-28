import sqlite3
import uuid
import os
import collections

class DataOps(object):
    """all the data operatiosn to my pi"""

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
       
    def saveHit(self, sensorId):
        curs = self.conn.cursor()
        dbStr = '''INSERT INTO Hits(Id,SensorId,Date,DeviceId) VALUES('{0}',{1},datetime('now'),'{2}');'''.format(uuid.uuid4(), sensorId, self.serialNum)
        curs.execute(dbStr)
        self.conn.commit()
        return

    def saveTemperature(self, sensorTemp):
        curs = self.conn.cursor()
        dbStr = '''INSERT INTO Temperatures(Id,SensorReading,Date,DeviceId) VALUES('{0}',{1},datetime('now'),'{2}');'''.format(uuid.uuid4(), sensorTemp, self.serialNum)
        curs.execute(dbStr)
        self.conn.commit()
        return

    def saveGpsData(self, gpsData):
        curs = self.conn.cursor()
        dbStr = '''INSERT INTO Locations(Id,Lat,Lon,Speed,Track,Date,DeviceId) VALUES('{0}',{1},{2},{3},{4},datetime('now'),'{5}');'''\
            .format(uuid.uuid4(), 
                    gpsData.lat, 
                    gpsData.lon,
                    gpsData.speed, 
                    gpsData.track, 
                    self.serialNum)
        curs.execute(dbStr)
        self.conn.commit()
        return
    
    def getGpsDatum(self):
        curs = self.conn.cursor()
        dbStr = '''SELECT Id,Lat,Lon,Speed,Track,Date,DeviceId FROM Locations;'''
        curs.execute(dbStr)
        rows = curs.fetchall()
        return rows
    
    def getGpsDatum(self):
        curs = self.conn.cursor()
        dbStr = '''SELECT * FROM Temperatures;'''
        curs.execute(dbStr)
        rows = curs.fetchall()
        return rows

    serialNum = "0000000000000000"
    conn = sqlite3.connect('tester.db', check_same_thread=False)
    conn.row_factory = dict_factory
    

    def _getserial_(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000001"
        try:
            strPath = '/proc/cpuinfo'
            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath,"..", "..", "..", strPath))
            f = open(filepath, "r")
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            f.close()
        except Exception as e:
            print(e)
            cpuserial = "ERROR000000004"        
        
        self.serialNum = cpuserial
        return self.serialNum
    
    def __init__(self):
        self._getserial_()

    def __delattr__(self):
        self.conn.close()
