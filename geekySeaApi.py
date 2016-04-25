from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "GeekySea Landing.  Welcome Aboard!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=99, debug=True)