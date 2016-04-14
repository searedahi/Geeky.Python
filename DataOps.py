import sqlite3
import uuid
import os

class DataOps(object):
    """all the data operatiosn to my pi"""
    serialNum = "0000000000000000"
    conn = sqlite3.connect('tester.db', check_same_thread=False)
       
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
        print(gpsData)
        curs = self.conn.cursor()
        dbStr = '''INSERT INTO Locations(Id,Lat,Lon,Date,DeviceId) VALUES('{0}',{1},{2},datetime('now'),'{3}');'''.format(uuid.uuid4(), gpsData.lat, gpsData.lon, self.serialNum)
        print(dbStr)
        curs.execute(dbStr)
        self.conn.commit()
        return

    def getserial(self):
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000001"
        try:
            strPath ='/proc/cpuinfo'
            basepath = os.path.dirname(__file__)
            filepath = os.path.abspath(os.path.join(basepath,"..", "..", "..", strPath))
            f = open(filepath, "r")
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
            f.close()
        except Exception as e:
            print (e)
            cpuserial = "ERROR000000004"        
        
        self.serialNum = cpuserial
        return self.serialNum
    
    def __init__(self):
        self.getserial()

    def __delattr__(self):
        self.conn.close()
