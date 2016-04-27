from flask import Flask, render_template, json, jsonify
import datetime
import RPi.GPIO as GPIO
import DataOps


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)


@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'Geeky Sea!',
      'time': timeString
      }
   return render_template('GeekyLanding.html', **templateData)


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




@app.route('/locations', methods = ['GET'])
def api_locations():

    locs = []

    locs = DataOps.DataOps.getGpsDatum()
    
    rsp = jsonify(loc=[e.serialize() for e in locs])
    
    return rsp


class SimpleUser(object):
    Id = -1
    FirstName = ''
    LastName = ''
    
    def serialize(self):
        return {
            'Id': self.Id, 
            'FirstName': self.FirstName,
            'LastName': self.LastName,
        }
    pass

@app.route('/users/<userid>', methods = ['GET'])
def api_users(userid):

    usersList = []
    for count in range(30):
        x = SimpleUser()
        x.Id = count
        x.FirstName = 'John'
        x.LastName = 'Somename'
        usersList.append(x)
    
    rsp = jsonify(usrs=[e.serialize() for e in usersList])
    
    return rsp


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










if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)