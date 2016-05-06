""" The main web server for geeky boating. """

import datetime
import RPi.GPIO as GPIO
import DataOps
import threading
import time

#services
import ThermometerService
import LocatorService

#webserver
from flask import Flask, render_template, json, jsonify, request
from flask.ext.classy import FlaskView
import TemperaturesView

#VS debugger
#import ptvsd
#ptvsd.enable_attach(secret='ApiServer')

class ApiServer(object):
    """ All the web and api calls and the flask wrapper. """
    app = Flask(__name__)
    GPIO.setmode(GPIO.BCM)
    runBackgroundApiThread = True

    TemperaturesView.register(app, route_base="/")



    #@app.route("/")
    #def landing():
    #   now = datetime.datetime.now()
    #   timeString = now.strftime("%Y-%m-%d %H:%M")       
    #   currF = 27
    #   templateData = {
    #      'title' : 'Geeky Sea!',
    #      'time': timeString,
    #      'tempF': currF
    #      }
    #   return render_template('GeekyLanding.html', **templateData) 

    #@app.route('/locations', methods = ['GET'])
    #def api_locations():
    #    dbRepo = DataOps.DataOps()
    #    locs = dbRepo.getGpsDatum()
    #    return json.dumps(locs)
    
    #@app.route('/temperatures', methods = ['GET'])
    #def api_tempuratures():
    #    dbRepo = DataOps.DataOps()
    #    temps = dbRepo.getTemperatures()
    #    return json.dumps(temps)

    #@app.route('/currentTemp', methods = ['GET'])
    #def api_currentTemp():
    #    Tempy = ThermometerService.ThermometerService()
    #    currF = Tempy.CurrentFarenheight()
    #    #currC = self.Tempy.CurrentCelcius()
    #    message = {
    #            'Farenheight': currF,
    #            'Celceius': 456,
    #    }
    #    resp = jsonify(message)
    #    resp.status_code = 200
    #    return resp




    
    #@app.route("/readPin/<pin>")
    #def readPin(pin):
    #   try:
    #      GPIO.setup(int(pin), GPIO.IN)
    #      if GPIO.input(int(pin)) == True:
    #         response = "Pin number " + pin + " is high!"
    #      else:
    #         response = "Pin number " + pin + " is low!"
    #   except:
    #      response = "There was an error reading pin " + pin + "."

    #   templateData = {
    #      'title' : 'Status of Pin' + pin,
    #      'response' : response
    #      }

    #   return render_template('PinStatus.html', **templateData)
    
    
    #@app.route('/messages', methods = ['POST'])
    #def api_message():

    #    if request.headers['Content-Type'] == 'text/plain':
    #        return "Text Message: " + request.data

    #    elif request.headers['Content-Type'] == 'application/json':
    #        return "JSON Message: " + json.dumps(request.json)

    #    else:
    #        return "415 Unsupported Media Type ;)"
    
    
    #@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
    #def api_echo():
    #    if request.method == 'GET':
    #        return "ECHO: GET\n"

    #    elif request.method == 'POST':
    #        return "ECHO: POST\n"

    #    elif request.method == 'PATCH':
    #        return "ECHO: PACTH\n"

    #    elif request.method == 'PUT':
    #        return "ECHO: PUT\n"

    #    elif request.method == 'DELETE':
    #        return "ECHO: DELETE"
    
            
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

    def _run_(self):
        self.app.run(host='0.0.0.0', port=80, debug=False)
        pass

    def __init__(self, apiTempy, apiLoco, interval=4):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.Tempy = apiTempy
        self.Loco = apiLoco

        self.interval = interval
        thread = threading.Thread(target=self._run_, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution