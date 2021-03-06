""" The main web server for geeky boating. """

import RPi.GPIO as GPIO
import time
import datetime

#services
from DataOps import DataOps
import ThermometerService
import LocatorService

#webserver
from flask import Flask, render_template, json, jsonify, request

#VS debugger
import ptvsd
ptvsd.enable_attach(secret='GeekyServer')


GPIO.setmode(GPIO.BCM)
TEMPSVC = ThermometerService.ThermometerService()
LOCASVC = LocatorService.LocatorService()
DBREPO = DataOps()

SERIALNUM = DBREPO.serial_num

app = Flask(__name__)

@app.route("/")
def landing():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    currF = TEMPSVC.current_farenheight()
    lat = LOCASVC.current_latitude()
    lon = LOCASVC.current_longitude()
    templateData = {
        'title' : 'Geeky Sea!',
        'time': timeString,
        'tempF': currF,
        'lat': lat,
        'lon': lon
        }
    return render_template('GeekyLanding.html', **templateData)

@app.route('/locations', methods = ['GET'])
def api_locations():
    locs = DBREPO.get_gps_datum()
    return json.dumps(locs)

@app.route('/temperatures', methods = ['GET'])
def api_tempuratures():
    try:
        temps = DBREPO.get_temperatures()
        return json.dumps(temps)
    except exce:
        print(exce)
        pass

@app.route('/temperatures/AboveDate/<minDate>}', methods = ['GET'])
def api_tempuratures_abovedate(minDate):
    try:
        temps = DBREPO.get_temperatures_above_date(minDate)
        return json.dumps(temps)
    except exce:
        print(exce)
        pass


@app.route('/currentTemp', methods = ['GET'])
def api_currentTemp():
    currF = TEMPSVC.current_farenheight()
    currC = TEMPSVC.current_celcius()
    message = {
            'Farenheight': currF,
            'Celceius': currC,
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp




@app.route("/readPin/<pin>")
def readPin(pin):
    try:
        GPIO.setup(int(pin), GPIO.IN)
        if GPIO.input(int(pin)) == True:
            response = "Pin number " + pin + " is high!"
        else:
            response = "Pin number " + pin + " is low!"
    except:
        response = "There was an error reading pin " + pin + "."

    templateData = {
        'title' : 'Status of Pin' + pin,
        'response' : response
        }

    return render_template('PinStatus.html', **templateData)
    
    
@app.route('/messages', methods = ['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    else:
        return "415 Unsupported Media Type ;)"
    
    
@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"





@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

app.error_handler_spec[None][404] = not_found

while LOCASVC.gps_data is None:
    print('Aquiring Satellites')
    time.sleep(5)

print('Starting Api Server')

app.run(host='0.0.0.0', port=80, debug=False)
