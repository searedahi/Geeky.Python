import sqlite3

class DataOps(object):
    """all the data operatiosn to my pi"""

    def getserial():
        # Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo','r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]
                    f.close()
        except:
            cpuserial = "ERROR000000000"        
        return cpuserial
    
    def saveHit(sensorId):
        conn = sqlite3.connect('tester.db')
        curs = conn.cursor()
        dbStr = '''INSERT INTO Hits(Id,SensorId,DeviceId) VALUES('{0}',{1},'{2}');'''.format(uuid.uuid4(), sensorId, getserial())
        curs.execute(dbStr)
        conn.commit()
        conn.close()
        return

    def saveTemperature(sensorTemp):
        conn = sqlite3.connect('tester.db')
        curs = conn.cursor()
        dbStr = '''INSERT INTO Temperatures(Id,SensorReading,DeviceId) VALUES('{0}',{1},'{2}');'''.format(uuid.uuid4(), sensorTemp, getserial())
        curs.execute(dbStr)
        conn.commit()
        conn.close()
        return

    def saveGpsData(gpsData):
        conn = sqlite3.connect('tester.db')
        curs = conn.cursor()
        dbStr = '''INSERT INTO Locations(Id,Lat,Lon,DeviceId) VALUES('{0}',{1},{2},'{3}');'''.format(uuid.uuid4(), gpsData.Lat, gpsData.Lon, getserial())
        curs.execute(dbStr)
        conn.commit()
        conn.close()
        return